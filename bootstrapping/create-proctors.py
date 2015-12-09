
import csv
import sys, getopt

def main(argv):
	# number of proctors to create
	n = 100
	usernamePrefix = "proctor"
	domainSuffix = "example.com"
	password = "password123"

	try:
		opts, args = getopt.getopt(argv, "hn:u:d:p:", ["help", "number=", "user=", "domain=", "password="])
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
		elif opt in ("-d", "--domain"):				
			domainSuffix = arg
			print "Proctor domain suffix = " + arg
		elif opt in ("-p", "--password"):
			password = arg
			print "Proctor password = " + arg

	#open students file for reading
	with open ('proctor_logins.csv', 'w') as csvfile:
		fieldnames = ['proctor_email', 'proctor_password']
		writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
		writer.writeheader()

		#SSID, Alt SSID must be unique
		for i in range(0, n):
			proctorNum = str(i)
			proctorEmail = usernamePrefix + proctorNum + "@" + domainSuffix
			writer.writerow({
				'proctor_email': proctorEmail, 
			    'proctor_password': password
			    })

def usage():
	print "Help/usage details:"
	print "  -n,  --number    : the number of proctors to create"
	print "  -u,  --user      : the username prefix of all proctor users"
	print "  -d   --domain    : the email domain suffix"
	print "  -p,  --password  : the password for all proctor users"
	print "  -h,  --help      : this help screen"



main(sys.argv[1:])
