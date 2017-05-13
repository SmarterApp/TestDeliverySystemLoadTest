import sys, getopt, os, csv


def main(argv):
    # DEFAULTS #
    # number of proctors to create
    n = 100
    usernamePrefix = "proctor"
    domainSuffix = "testing.com"
    password = "password123"
    distributed_mode = False

    try:
        opts, args = getopt.getopt(argv, "hn:u:d:p:d:",
                                   ["help", "number=", "user=", "domain=", "password=", "distributed="])
    except getopt.GetoptError:
        usage()
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage();
            sys.exit()
        elif opt in ("-n", "--number"):
            print "Number of proctors = " + arg
            n = int(arg)
        elif opt in ("-u", "--user"):
            usernamePrefix = arg
            print "Proctor username prefix = " + arg
        elif opt in ("-e", "--email"):
            domainSuffix = arg
            print "Proctor email domain suffix = " + arg
        elif opt in ("-p", "--password"):
            password = arg
            print "Proctor password = " + arg
        elif opt in ("-d", "--distributed"):
            distributed_mode = True
            server_host_filename = arg

    print "Creating proctor_logins.csv at current directory."
    # open proctors file for reading
    with open('proctor_logins.csv', 'w') as csvfile:
        fieldnames = ['proctor_email', 'proctor_password']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for i in range(0, n):
            proctorNum = str(i)
            proctorEmail = usernamePrefix + proctorNum + "@" + domainSuffix
            writer.writerow({
                'proctor_email': proctorEmail,
                'proctor_password': password
            })
    print "Created proctor seed file with " + str(n) + " proctors."

    if distributed_mode:
        # Get path of python file (where the jmeter_servers file should be located)
        __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

        # Get number of nodes (lines in jmeter_servers file) that we need to break csv file into
        num_nodes = sum(1 for line in open(os.path.join(__location__, 'jmeter_servers')) if line.rstrip())
        print "Number of nodes detected in jmeter_servers file: " + str(num_nodes)

        # Split students into student_logins_<n>.csv so that each file can be SCP'd to host systems.
        split(open('proctor_logins.csv', 'r'), ',', n / num_nodes, 'proctor_logins_%s.csv');

        # Iterate over each server hostname and scp the seed file to the node
        with open(os.path.join(__location__, server_host_filename)) as jmeter_servers:
            for i, line in enumerate(jmeter_servers):
                host = str(line).strip()
                # Get partition seed file path
                proctor_logins_part_path = "./proctor_logins_" + str(i + 1) + ".csv"
                print "Switching over to the loadtest docker env"
                #subprocess.Popen()
                print "Executing SCP transfer of proctor_logins_" + str(i + 1) + ".csv to host " + host + "..."
                # Do a docker cp into the jmeter-server containers
                os.system('eval "$(docker-machine env --swarm tds-jmeter-client)" && ' +
                    'docker cp ' + proctor_logins_part_path + ' ' + host + ':/usr/local/apache-jmeter-2.13/proctor_logins.csv')
                print "Transfer to host " + host + " has completed. Cleaning up " + proctor_logins_part_path + "..."
                os.remove(proctor_logins_part_path)
                print "Cleanup complete!"


def usage():
    print "Help/usage details:"
    print "  -n,  --number    	: the number of proctors to create"
    print "  -u,  --user      	: the username prefix of all proctor users"
    print "  -e   --email    	: the email domain suffix"
    print "  -p,  --password  	: the password for all proctor users"
    print "  -h,  --help      	: this help screen"
    print "  -d,  --distributed	: distributed mode - the file provided in the argument will be read to indicate how many pieces" \
          " the seed file should be broken into and will be sent to the host addresses in this file. Should be followed by path of ssh key"


def split(filehandler, delimiter=',', row_limit=10000,
          output_name_template='output_%s.csv', output_path='.', keep_headers=True):
    """
    Splits a CSV file into multiple pieces.

    A quick bastardization of the Python CSV library.
    Arguments:
        `row_limit`: The number of rows you want in each output file. 10,000 by default.
        `output_name_template`: A %s-style template for the numbered output files.
        `output_path`: Where to stick the output files.
        `keep_headers`: Whether or not to print the headers in each output file.
    Example usage:

        >> from toolbox import csv_splitter;
        >> csv_splitter.split(open('/home/ben/input.csv', 'r'));

    """
    import csv
    reader = csv.reader(filehandler, delimiter=delimiter)
    current_piece = 1
    current_out_path = os.path.join(
        output_path,
        output_name_template % current_piece
    )
    current_out_writer = csv.writer(open(current_out_path, 'w'), delimiter=delimiter)
    current_limit = row_limit
    if keep_headers:
        headers = reader.next()
        current_out_writer.writerow(headers)
    for i, row in enumerate(reader):
        if i + 1 > current_limit:
            current_piece += 1
            current_limit = row_limit * current_piece
            current_out_path = os.path.join(
                output_path,
                output_name_template % current_piece
            )
            current_out_writer = csv.writer(open(current_out_path, 'w'), delimiter=delimiter)
            if keep_headers:
                current_out_writer.writerow(headers)
        current_out_writer.writerow(row)


main(sys.argv[1:])
