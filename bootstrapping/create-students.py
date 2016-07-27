import pymongo, csv, sys, getopt, random, os, json, datetime

from pymongo import MongoClient


def main(argv):
    # Assume non-distributed mode
    distributed_mode = False

    # number of students to create
    n = 3000

    # institution
    institution_ids = []

    # grade levels
    grade_levels = []

    # default connection string
    connection = "mongodb://username:password@ip_of_mongodb:27017/art"

    format = "csv"

    mode = "create"

    errors = False

    try:
        opts, args = getopt.getopt(argv, "hn:i:g:c:d:f:m:e:",
                                   ["help", "number=", "institutions="
                                       , "grades=", "connection=", "distributed=", "format=", "mode=", "errors="])
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
        elif opt in ("-d", "--distributed"):
            distributed_mode = True
            server_host_filename = arg
        elif opt in ("-f", "--format"):
            print "Format = " + arg
            format = arg
        elif opt in ("-m", "--mode"):
            print "Mode = " + arg
            mode = arg
        elif opt in ("-e", "--errors"):
            print "Errors = " + arg
            errors = arg

    if format != "json":
        format = "csv"

    if mode != "delete":
        mode = "create"

    errors = (errors == "true" or errors == "True" or errors)

    # default to grades 3-12 if none provided
    if (len(grade_levels) == 0):
        grade_levels = range(3, 12)
    # Assume this file is for use with ART import as well as loadtest
    loadtest_only = False
    try:
        client = MongoClient(connection)
        db = client.art

        # get the matching institutions objects
        if (len(institution_ids) != 0):
            institutions = list(db.institutionEntity.find({"entityId": {"$in": institution_ids}}))
        else:
            institutions = list(db.institutionEntity.find({}))

        total_institutions = len(institutions)
    except:
        # For loadtest, the institutions don't matter, only usernames and firstnames are read.
        loadtest_only = True
        print "Unable to connect to ART mongodb to obtain institution/entity information."
        print "A seed file will still be generated, but will not be importable in ART."

    # clean up grade levels to make sure that they are 2 digits
    for idx, grade in enumerate(grade_levels):
        grade_levels[idx] = "{0:0>2}".format(grade_levels[idx])
    total_grade_levels = len(grade_levels)

    if format == "csv":
        print "Creating student_logins.csv at current directory."
        # open students file for reading
        with open('student_logins.csv', 'w') as csvfile:
            fieldnames = ['StateAbbreviation', 'ResponsibleDistrictIdentifier', 'ResponsibleInstitutionIdentifier',
                          'LastOrSurname', 'FirstName', 'MiddleName',
                          'Birthdate', 'SSID', 'ExternalSSID', 'GradeLevelWhenAssessed', 'Sex',
                          'HispanicOrLatinoEthnicity',
                          'AmericanIndianOrAlaskaNative', 'Asian',
                          'BlackOrAfricanAmerican', 'White', 'NativeHawaiianOrOtherPacificIslander',
                          'DemographicRaceTwoOrMoreRaces', 'IDEAIndicator', 'LEPStatus',
                          'Section504Status', 'EconomicDisadvantageStatus', 'LanguageCode',
                          'EnglishLanguageProficiencyLevel', 'MigrantStatus', 'FirstEntryDateIntoUSSchool',
                          'LimitedEnglishProficiencyEntryDate', 'LEPExitDate', 'TitleIIILanguageInstructionProgramType',
                          'PrimaryDisabilityType', 'Delete']

            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            # SSID, Alt SSID must be unique
            for i in range(0, n):
                studentNum = str(i)
                if loadtest_only:
                    institutionObject = {'parentEntityId': 'TEST', 'entityId': 'TEST'}
                else:
                    institutionObject = institutions[random.randint(0, total_institutions - 1)]
                grade_level = grade_levels[random.randint(0, total_grade_levels - 1)]

                # the 6 race options are all set to NO to start, then we randomly make 1 YES
                race = ["NO", "NO", "NO", "NO", "NO", "NO"]
                race[random.randint(0, 5)] = "YES"

                writer.writerow({
                    'StateAbbreviation': 'OR',
                    'ResponsibleDistrictIdentifier': institutionObject['parentEntityId'],
                    'ResponsibleInstitutionIdentifier': institutionObject['entityId'],
                    'LastOrSurname': 'LastName' + studentNum,
                    'FirstName': 'Name' + studentNum,
                    'MiddleName': 'MiddleName' + studentNum,
                    'Birthdate': '',
                    'SSID': 'ASTDNT' + studentNum,
                    'ExternalSSID': 'STDNT' + studentNum,
                    'GradeLevelWhenAssessed': grade_level,
                    'Sex': "Female" if random.randint(0, 1) == 0 else "Male",  # 50/50 male/female
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
                    'Delete': ''
                })
        print "Created student seed file with " + str(n) + " students."

        if distributed_mode:
            # Get path of python file (where the jmeter_servers file should be located)
            __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

            # Get number of nodes (lines in jmeter_servers file) that we need to break csv file into
            num_nodes = sum(1 for line in open(os.path.join(__location__, 'jmeter_servers')) if line.rstrip())
            print "Number of nodes detected in jmeter_servers file: " + str(num_nodes)

            # Split students into student_logins_<n>.csv so that each file can be SCP'd to host systems.
            split(open('student_logins.csv', 'r'), ',', n / num_nodes, 'student_logins_%s.csv');

            # Iterate over each server hostname and scp the seed file to the node
            with open(os.path.join(__location__, server_host_filename)) as jmeter_servers:
                for i, line in enumerate(jmeter_servers):
                    host = str(line).strip()
                    # Get partition seed file path
                    student_logins_part_path = "./student_logins_" + str(i + 1) + ".csv"
                    print "Executing SCP transfer of student_logins_" + str(i + 1) + ".csv to host " + host + "..."
                    # Do a docker cp into the jmeter-server containers
                    os.system('eval "$(docker-machine env --swarm tds-jmeter-client)" && ' +
                              'docker cp ' + student_logins_part_path + ' ' + host + ':/usr/local/apache-jmeter-2.13/student_logins.csv')
                    print "Transfer to host " + host + " has completed. Cleaning up " + student_logins_part_path + "..."
                    os.remove(student_logins_part_path)
                    print "Cleanup complete!"
    elif format == "json" and mode == "create":
        print "Creating jsonStudents.txt at current directory"

        data = []

        dayseperator = 1501 if errors else 2000

        for i in range(0, n):
            studentNum = str(i)
            if loadtest_only:
                institutionObject = {'parentEntityId': 'TEST', 'entityId': 'TEST'}
            else:
                institutionObject = institutions[random.randint(0, total_institutions - 1)]
            grade_level = grade_levels[random.randint(0, total_grade_levels - 1)]

            # the 6 race options are all set to false to start, then we randomly make 1 true
            race = [False, False, False, False, False, False]
            race[random.randint(0, 5)] = True

            # This is a StudentDto as required by the batching API
            data.append({
                "ssid": 'ASTDNT' + studentNum,
                "stateAbbreviation": "CA",
                "institutionIdentifier": institutionObject['entityId'],
                "districtIdentifier": institutionObject['parentEntityId'],
                "firstName": 'Name' + studentNum,
                "lastName": 'LastName' + studentNum,
                "middleName": 'MiddleName' + studentNum,
                "birthDate": datetime.date.fromordinal(
                    datetime.date.today().toordinal() - random.randint(dayseperator, 3000)).strftime("%F"),
                "externalSsid": 'STDNT' + studentNum,
                "gradeLevelWhenAssessed": grade_level,
                "sex": "Female" if random.randint(0, 1) == 0 else "Male",
                "hispanicOrLatino": race[0],
                "americanIndianOrAlaskaNative": race[1],
                "asian": race[2],
                "blackOrAfricanAmerican": race[3],
                "white": race[4],
                "nativeHawaiianOrPacificIsland": race[5],
                "twoOrMoreRaces": False if random.randint(0, 1) == 0 else True,
                "iDEAIndicator": False if random.randint(0, 1) == 0 else True,
                "lepStatus": False if random.randint(0, 1) == 0 else True,
                "section504Status": False if random.randint(0, 1) == 0 else True,
                "disadvantageStatus": False if random.randint(0, 1) == 0 else True,
                "languageCode": None,
                "migrantStatus": False if random.randint(0, 1) == 0 else True,
                "firstEntryDateIntoUsSchool": datetime.date.fromordinal(
                    datetime.date.today().toordinal() - random.randint(1, 1500)).strftime("%F"),
                "lepEntryDate": None,
                "lepExitDate": None,
                "title3ProgramType": None,
                "primaryDisabilityType": None,
                "elpLevel": 0
            })

        with open('jsonStudents.txt', 'w') as outfile:
            json.dump(data, outfile)

    elif format == "json" and mode == "delete":
        print "Creating jsonStudentsDelete.txt at current directory"

        data = []

        for i in range(0, n):
            studentNum = str(i)

            data.append({
                "ssid": 'ASTDNT' + studentNum,
                "stateCode": "CA"
            })

        with open('jsonStudentsDelete.txt', 'w') as outfile:
            json.dump(data, outfile)

    else:
        print "Invalid format"


def usage():
    print "Help/usage details:"
    print "  -c, --connection 	: mongo connection string (defaults to mongodb://localhost:27017/)"
    print "  -n, --number     	: the number of students to create"
    print "  -d, --distributed	: distributed mode - the file provided in the argument will be read to indicate how many pieces" \
          " the seed file should be broken into and will be sent to the host addresses in this file. Should be followed by path of ssh key"
    print "  --institutions   	: comma separated list of institution entityIds to use (from the institutionEntity collection). if none provided it will use all available"
    print "  --grades         	: comma separated list of grade levels to choose from. if none provided it will use 3-12"
    print "  -h, --help       	: this help screen"


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
