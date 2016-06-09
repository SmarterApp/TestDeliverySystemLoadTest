import subprocess, os, sys, getopt, re, time, shutil
import boto.ec2


def main(argv):
    # Defaults
    students_per_proctor = 10
    total_students = 20
    num_workers = 2

    try:
        opts, args = getopt.getopt(argv, "hs:p:w:g:c", ["help", "students=", "proctors=", "workers=", "cleanup"])
    except getopt.GetoptError:
        usage()
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage();
            sys.exit()
        elif opt in ("-c", "--cleanup"):
            cleanup()
            sys.exit()
        elif opt in ("-s", "--students"):
            print "Number of students = " + arg
            total_students = int(arg)
        elif opt in ("-p", "--proctors"):
            print "Number of students per proctor = " + arg
            students_per_proctor = int(arg)
        elif opt in ("-w", "--workers"):
            print "Number of JMeter Workers = " + arg
            num_workers = int(arg)

    total_proctors = total_students / students_per_proctor
    # The path should be the first (only) argument
    loadtest_jmx_path = args[0]

    if not os.path.isfile(loadtest_jmx_path) or not loadtest_jmx_path.endswith(".jmx"):
        print "File path provided does not exist or is not a JMX file."
        sys.exit(-1)

    print "Starting automated tds-loadtest deployment..."

    tmp_loadtest_jmx_path = create_loadtest_copy(loadtest_jmx_path, num_workers, total_students, students_per_proctor)
    start_docker_daemon()
    create_and_start_client_container()
    server_ips = create_and_start_server_containers(num_workers)
    update_test_sg('tds-jmeter-sg')
    client_ip = configure_client_machine(tmp_loadtest_jmx_path)
    create_and_distribute_seed_data(total_proctors, total_students)
    launch_worker_execute_test(client_ip, server_ips)

    print "Container ID of the loadtest jmeter docker containers:\n"
    os.system('eval "$(docker-machine env --swarm tds-jmeter-client)" && docker ps')

    print "\nRun the command \"docker logs -f <client container id>\" to begin monitoring the load test."
    print "When the test concludes, run the command \"docker-machine scp tds-jmeter-client:/load_tests/tds-loadtest.jtl .\" " \
          "to copy the file to the current directory."


def cleanup():
    print "Starting tds-loadtest environment cleanup..."
    docker_remote_instances = subprocess.check_output(['docker-machine', 'ls', '-q']).splitlines()
    for instance in docker_remote_instances:
        if "tds-jmeter" in instance:
            print "Removing docker remote instance " + instance
            os.system("docker-machine rm -f " + instance)

    print "Cleanup completed. All active jmeter AWS EC2 instances will be terminated momentarily."

def create_loadtest_copy(loadtest_jmx_path, num_workers, total_students, students_per_proctor):
    # Step 1 - Create a copy of the loadtest file and replace student count in copy
    tmp_loadtest_jmx_path = "/tmp/tds-loadtest.jmx"
    print "Copying original jmx file at " + loadtest_jmx_path + ' to ' + tmp_loadtest_jmx_path
    # Copy the loadtest jmx file to the tmp directory.
    shutil.copy2(loadtest_jmx_path, tmp_loadtest_jmx_path)
    # Replace the TOTAL_STUDENT_COUNT variable with the actual total # of students / # of worker nodes
    os.system(
        "sed -i -e 's/\${TOTAL_STUDENT_COUNT}/" + str(total_students / num_workers) + "/g' " + tmp_loadtest_jmx_path)
    # Replace the STUDENTS_PER_PROCTOR with the amount provided in the script arguments
    os.system(
        "sed -i -e 's/\${STUDENTS_PER_PROCTOR}/" + str(students_per_proctor) + "/g' " + tmp_loadtest_jmx_path)
    students_per_proctor
    return tmp_loadtest_jmx_path


def start_docker_daemon():
    # Step 2 - Start docker daemon
    print "Starting docker daemon..."
    os.system('docker-machine start default')
    os.system('eval "$(docker-machine env default)"')
    print "Docker daemon is started!"


def create_and_start_client_container():
    # Step 3 - run the script to create jmeter client (master) node
    print "Creating tds-jmeter-client (master) ec2 instance and deploying the docker image..."
    os.system('./launch_jmeter_client_aws')
    print "Finished configuring tds-jmeter-client"


def create_and_start_server_containers(num_workers):
    # Step 4 - run the script to create the jmeter server (worker) node(s)
    print "Creating tds-jmeter-server(s) ec2 instance(s) and deploying the docker images..."
    launch_server_output = subprocess.check_output(['./launch_jmeter_server_aws', str(num_workers)])
    # Extract the server ips from the script output
    server_ips = re.search("Server IP's, for use in JMeter Client: (.*)", launch_server_output).group(1)
    print "Finished creating and configuring jmeter-servers. Server IPs: " + server_ips
    return server_ips


def update_test_sg(sg_name):
    # Step 5 - Update the tds-jmeter-sg security group to open port 1099 (for communication between jmeter nodes)
    with open("app_aws.env", 'r') as appconfig:
        region = [line.split('=')[1].strip() for line in appconfig if line.startswith("export AWS_DEFAULT_REGION=")][0]
    try:
        conn=boto.ec2.connect_to_region(region)
        dm_sg_group = [g for g in conn.get_all_security_groups() if g.name == sg_name][0]
        if not any(rule.from_port == '1099' for rule in dm_sg_group.rules):
            conn.authorize_security_group(sg_name,
                                          ip_protocol='TCP',
                                          from_port=1099,
                                          to_port=1099,
                                          cidr_ip='0.0.0.0/0')
    except:
        print "Error connecting to ec2 using boto or updating docker-machine security group in AWS"


def configure_client_machine(loadtest_jmx_path):
    # Step 6 - Creating load tests directory in jmeter-client and setting permissions, and then copying tds-loadtest.jmx file over
    print "Creating load test directory in tds-jmeter-client and setting folder permissions."
    os.system('eval "$(docker-machine env --swarm tds-jmeter-client)"')
    os.system(
        'docker-machine ssh tds-jmeter-client "sudo mkdir -p /load_tests && sudo chown ubuntu:ubuntu /load_tests && exit"')
    print "Copying test directory (" + loadtest_jmx_path + " to tds-jmeter-client..."
    os.system('docker-machine scp ' + loadtest_jmx_path + ' tds-jmeter-client:/load_tests')
    client_ip = subprocess.check_output(['docker-machine', 'ip', 'tds-jmeter-client'])
    print "tds-jmeter-client ip = " + client_ip
    return client_ip.strip()


def create_and_distribute_seed_data(total_proctors, total_students):
    time.sleep(60)
    # Step 7 - Get container ids for workers and generate jmeter_servers file for use with seed data creation/distribution script
    print "Getting container ids from docker ps command..."
    subprocess.Popen(
        ['eval "$(docker-machine env --swarm tds-jmeter-client)" && docker ps -q > jmeter_servers']
        , stdout=subprocess.PIPE, shell=True).communicate()
    print "Finished creating container id file \"jmeter_servers\". Running student and proctor seed data creation and " \
          "distribution scripts..."
    # Step 8 - Create and distribute seed data scripts to each worker container
    os.system('python create-students.py -d jmeter_servers -n ' + str(total_students))
    os.system('python create-proctors.py -d jmeter_servers -n ' + str(total_proctors))
    os.remove('jmeter_servers')
    print "Finished distributing student and proctor seed data!"


def launch_worker_execute_test(client_ip, server_ips):
    # Step 9 - Start the loadtest
    print "Ready for liftoff! - time to run tds-jmeter-client and fire off the load test, and grab some more coffee. "
    os.system('eval "$(docker-machine env --swarm tds-jmeter-client)" && docker run ' +
              '  --detach ' +
              '  --publish 1099:1099 ' +
              '  --volume /load_tests:/load_tests ' +
              '  --env TEST_DIR="." ' +
              '  --env TEST_PLAN="tds-loadtest" ' +
              '  --env IP="' + client_ip + '" '
              '  --env REMOTE_HOSTS="' + server_ips + '" '
              '  --env constraint:type==client ' +
              '  hhcordero/docker-jmeter-client')


def usage():
    print "Help/usage details:"
    print "  -w, --workers 	    : the number of worker (server) nodes to create and use for the load test"
    print "  -s, --students     : the number of students to create"
    print "  -p, --proctors     : the number of students per proctors"
    print "  -c, --cleanup      : run the cleanup procedure, which terminates all jMeter related ec2 instances in AWS"
    print "  -h, --help       	: this help screen"


main(sys.argv[1:])
