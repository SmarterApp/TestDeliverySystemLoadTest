import pymongo
import sys, getopt, random

from pymongo import MongoClient

def main(argv):
	# number of students to create
	n = 1

	# institution
	institution_ids = []
	institutions = []

	#grade levels
	grade_levels = []

	# connection string
	connection = "mongodb://localhost:27017/"

	try:
		opts, args = getopt.getopt(argv, "hn:i:g:", ["help", "number=", "institutions=", "grades="])
	except getopt.GetoptError:
		usage()
		sys.exit(2)

	for opt, arg in opts:
		if opt in ("-h", "--help"):
			usage();
			sys.exit()
		elif opt in ("-n", "--number"):
			print "Number of students = " + arg
			n = int(arg)
		elif opt in ("-i", "--institutions"):
			print "Institutions = " + arg
			institution_ids = arg.split(',')
		elif opt in ("-c", "--connection"):
			print "Connection string = " + arg
			connection = arg
		elif opt in ("-g", "--grades"):
			print "Grades = " + arg
			grade_levels = arg.split(',')


	# TODO: add validation checking and call usage() if we don't have valid data

	client = MongoClient(connection)
	db = client.local

	# clean up grade levels to make sure that they are 2 digits
	for idx, grade in enumerate(grade_levels):
		grade_levels[idx] = "{0:0>2}".format(grade_levels[idx])

	# get the matching institutions objects
	# TODO: change this to do 1 query to get all items 
	for institutionId in institution_ids:
		institutionObject = db.institutionEntity.find_one({ "entityId" : institutionId})
		print "Looking up " + institutionId + " details"
		
		if institutionObject is not None:
			institutions.append(institutionObject);
	
	total_grade_levels = len(grade_levels)
	total_institutions = len(institutions)
	new_students = []

	for i in xrange(1, n+1):
		student_num = str(i)
		institutionObject = institutions[random.randint(0, total_institutions-1)]
		grade_level = grade_levels[random.randint(0, total_grade_levels-1)]

		# the 7 race options are all set to NO to start, then we randomly make 1 YES
		race = ["NO","NO","NO","NO","NO","NO","NO"]
		race[random.randint(0,6)] = "YES"

		new_students.append({
		    "_class" : "org.opentestsystem.delivery.testreg.domain.Student",
		    "stateAbbreviation" : institutionObject['stateAbbreviation'],
		    "entityId" : "ssid" + student_num,
		    "institutionIdentifier" : institutionObject['entityId'],
		    "institutionEntityMongoId" : str(institutionObject['_id']),
		    "districtIdentifier" : institutionObject['parentEntityId'],
		    "districtEntityMongoId" : institutionObject['parentId'],
		    "firstName" : "FirstName" + student_num,
		    "lastName" : "LastName" + student_num,
		    "externalSsid" : "assid" + student_num,
		    "gradeLevelWhenAssessed" : grade_level,
		    "gender" : "Female" if random.randint(0, 1) == 0 else "Male", # 50/50 male/female
		    "hispanicOrLatino" : race[0],
		    "americanIndianOrAlaskaNative" : race[1],
		    "asian" : race[2],
		    "blackOrAfricanAmerican" : race[3],
		    "white" : race[4],
		    "nativeHawaiianOrPacificIsland" : race[5],
		    "twoOrMoreRaces" : race[6],
		    "iDEAIndicator" : "NO",
		    "lepStatus" : "NO",
		    "section504Status" : "NO",
		    "disadvantageStatus" : "NO",
		    "migrantStatus" : "NO",
		    "accommodations" : [ 
		        {
		            "studentId" : "ssid" + student_num,
		            "stateAbbreviation" : institutionObject['stateAbbreviation'],
		            "subject" : "ELA"
		        }, 
		        {
		            "studentId" : "ssid" + student_num,
		            "stateAbbreviation" : institutionObject['stateAbbreviation'],
		            "subject" : "MATH"
		        }
		    ],
		    "race" : "",
		    "studentPackageVersion" : 2.0000000000000000,
		    "inValidAccommodationsSubject" : False
		    #"languageCode" : "eng"
		    #"primaryDisabilityType" : "AUT"
		})

		# do batches of 500
		if i % 500 == 0:
			db.student.insert_many(new_students)
			new_students = []

	# insert any that are left over
	if len(new_students) != 0:
		db.student.insert_many(new_students)


def usage():
	print "Help/usage details:"
	print "  -c, --connection : mongo connection string (defaults to mongodb://localhost:27017/)"
	print "  -n, --number     : the number of students to create"
	print "  --institutions   : comma separated list of institution entityIds to use (from the institutionEntity collection"
	print "  --grades         : comma separated list of grade levels to choose from"
	print "  -h, --help       : this help screen"



main(sys.argv[1:])
