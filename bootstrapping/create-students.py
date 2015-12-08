import pymongo
import csv
import sys, getopt, random

from pymongo import MongoClient

def main(argv):
	# number of students to create
	n = 500

	# institution
	institution_ids = []
	institutions = []

	#grade levels
	grade_levels = []

	# default connection string
	connection = "mongodb://mongo_admin:password123@52.32.66.151:27017/art"

	try:
		opts, args = getopt.getopt(argv, "hn:i:g:c:", ["help", "number=", "institutions=", "grades=", "connection="])
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

	# default to grades 3-12 if none provided
	if (len(grade_levels) == 0):
		grade_levels = range(3, 12)

	client = MongoClient(connection)
	db = client.art

	# clean up grade levels to make sure that they are 2 digits
	for idx, grade in enumerate(grade_levels):
		grade_levels[idx] = "{0:0>2}".format(grade_levels[idx])

	# get the matching institutions objects
	if (len(institution_ids) != 0):
		institutions = list(db.institutionEntity.find({ "entityId" : { "$in" : institution_ids } }))
	else:
		institutions = list(db.institutionEntity.find({}))
	
	total_grade_levels = len(grade_levels)
	total_institutions = len(institutions)
	new_students = []

	#open students file for reading
	with open ('student_logins.csv', 'w') as csvfile:
		fieldnames = ['StateAbbreviation', 'ResponsibleDistrictIdentifier', 'ResponsibleInstitutionIdentifier', 'LastOrSurname', 'FirstName', 'MiddleName',
		'Birthdate', 'SSID', 'AlternateSSID', 'GradeLevelWhenAssessed', 'Sex', 'HispanicOrLatinoEthnicity', 'AmericanIndianOrAlaskaNative', 'Asian', 
		'BlackOrAfricanAmerican', 'White', 'NativeHawaiianOrOtherPacificIslander', 'DemographicRaceTwoOrMoreRaces', 'IDEAIndicator', 'LEPStatus', 
		'Section504Status', 'EconomicDisadvantageStatus', 'LanguageCode', 'EnglishLanguageProficiencyLevel', 'MigrantStatus', 'FirstEntryDateIntoUSSchool',
		'LimitedEnglishProficiencyEntryDate', 'LEPExitDate', 'TitleIIILanguageInstructionProgramType', 'PrimaryDisabilityType', 'Delete']
		
		writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
		writer.writeheader()

		#SSID, Alt SSID must be unique
		for i in range(0, n):
			studentNum = str(i)
			institutionObject = institutions[random.randint(0, total_institutions-1)]
			grade_level = grade_levels[random.randint(0, total_grade_levels-1)]

			# the 6 race options are all set to NO to start, then we randomly make 1 YES
			race = ["NO","NO","NO","NO","NO","NO"]
			race[random.randint(0,5)] = "YES"

			writer.writerow({
				'StateAbbreviation': institutionObject['stateAbbreviation'], 
				'ResponsibleDistrictIdentifier': institutionObject['parentEntityId'], 
				'ResponsibleInstitutionIdentifier': institutionObject['entityId'],
				'LastOrSurname': 'LastName' + studentNum, 
				'FirstName': 'FirstName' + studentNum, 
				'MiddleName': 'MiddleName' + studentNum,
				'Birthdate': '', 
				'SSID': 'STUDENT' + studentNum, 
				'AlternateSSID': 'ASTUDENT' + studentNum, 
				'GradeLevelWhenAssessed': grade_level, 
				'Sex': "Female" if random.randint(0, 1) == 0 else "Male", # 50/50 male/female
				'HispanicOrLatinoEthnicity': race[0],
				'AmericanIndianOrAlaskaNative': race[1], 
				'Asian': race[2], 
				'BlackOrAfricanAmerican': race[3], 
				'White': race[4], 
				'NativeHawaiianOrOtherPacificIslander': race[5],
				'DemographicRaceTwoOrMoreRaces': 'NO', 
				'IDEAIndicator': 'NO', 
				'LEPStatus': 'NO', 
				'Section504Status': 'NO', 
				'EconomicDisadvantageStatus': 'NO',
				'LanguageCode': '', 
				'EnglishLanguageProficiencyLevel': '', 
				'MigrantStatus': 'NO', 
				'FirstEntryDateIntoUSSchool': '', 
				'LimitedEnglishProficiencyEntryDate': '',
				'LEPExitDate': '', 
				'TitleIIILanguageInstructionProgramType': '', 
				'PrimaryDisabilityType': '',
				'Delete': '' })

def usage():
	print "Help/usage details:"
	print "  -c, --connection : mongo connection string (defaults to mongodb://localhost:27017/)"
	print "  -n, --number     : the number of students to create"
	print "  --institutions   : comma separated list of institution entityIds to use (from the institutionEntity collection). if none provided it will use all available"
	print "  --grades         : comma separated list of grade levels to choose from. if none provided it will use 3-12"
	print "  -h, --help       : this help screen"



main(sys.argv[1:])
