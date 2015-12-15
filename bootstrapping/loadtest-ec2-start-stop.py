import boto.ec2
import sys, getopt
import copy
import time

env_tag = "LoadTest"
admin_managed_tag = "StartStop"

def main(argv):
	action = argv[0]

	if (action == "start"):
		process_instances("start")
	elif (action == "stop"):
		process_instances("stop")
	else:
		print "Need to pass in either start or stop"



# ref: http://www.imlucas.com/post/55003805078/waiting-for-instances-to-start-with-python-and
def wait_for_instances_to_start(conn, instance_ids, pending_ids):
    """Loop through all pending instace ids waiting for them to start.
        If an instance is running, remove it from pending_ids.
        If there are still pending requests, sleep and check again in 10 seconds.
        Only return when all instances are running."""
    reservations = conn.get_all_instances(instance_ids=pending_ids)
    for reservation in reservations:
        for instance in reservation.instances:
            if instance.state == 'running':
                print "instance `{}` running!".format(instance.id)
                pending_ids.pop(pending_ids.index(instance.id))
            else:
                print "instance `{}` starting...".format(instance.id)
    if len(pending_ids) == 0:
        print "all instances started!"
    else:
        time.sleep(10)
        wait_for_instances_to_start(conn, instance_ids, pending_ids)

def process_instances(action):
	# go through all regions
	for region in boto.ec2.regions():
		try:
			conn=boto.ec2.connect_to_region(region.name)
			reservations = conn.get_all_instances()	
			first_instance_ids = []
			second_instance_ids = []
			third_instance_ids = []
			for res in reservations:
				for inst in res.instances:

					name = inst.tags['Name'] if 'Name' in inst.tags else None
					state = inst.state
					env_value = inst.tags['Environment'] if 'Environment' in inst.tags else None
					admin_managed_value = inst.tags['AdminManaged'] if 'AdminManaged' in inst.tags else None
					priority = inst.tags['AdminManagedPriority'] if 'AdminManagedPriority' in inst.tags else '3'

					#print "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s" % (region.name, name, inst.id, inst.instance_type, inst.launch_time, state, env_value, admin_managed_value, inst.tags)

					#print "%s\t%s" % (admin_managed_value, env_value)
					if admin_managed_value == admin_managed_tag and env_value == env_tag and ((state == "stopped" and action == "start") or (state == "running" and action == "stop")):
						if priority == "1":
							first_instance_ids.append(inst.id)
						elif priority == "2":
							second_instance_ids.append(inst.id)
						elif priority == "3":
							third_instance_ids.append(inst.id)

					
			if action == "start":
				if len(first_instance_ids) > 0:
					print "Starting the priority 1 instances"
					conn.start_instances(instance_ids=first_instance_ids, dry_run=False)
					print "Waiting for the priority 1 instances"
					wait_for_instances_to_start(conn, first_instance_ids, copy.deepcopy(first_instance_ids))
					print "Priority 1 instances started"

				if len(second_instance_ids) > 0:
					print "Starting the priority 2 instances"
					conn.start_instances(instance_ids=second_instance_ids, dry_run=False)
					print "Waiting for the priority 2 instances"
					wait_for_instances_to_start(conn, second_instance_ids, copy.deepcopy(second_instance_ids))
					print "Priority 2 instances started"

				if len(third_instance_ids) > 0:
					print "Starting the priority 3 instances"
					conn.start_instances(instance_ids=third_instance_ids, dry_run=False)
					print "Waiting for the priority 3 instances"
					wait_for_instances_to_start(conn, third_instance_ids, copy.deepcopy(third_instance_ids))
					print "Priority 3 instances started"


			elif action == "stop":
				print "Stopping all instances"
				conn.stop_instances(instance_ids=first_instance_ids, dry_run=False)
				conn.stop_instances(instance_ids=second_instance_ids, dry_run=False)
				conn.stop_instances(instance_ids=third_instance_ids, dry_run=False)



		# most likely will get exception on new beta region and gov cloud
		except Exception as e:
			print 'Exception error in %s: %s' % (region.name, e.message)


main(sys.argv[1:])