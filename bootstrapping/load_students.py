import requests, sys, getopt, random, os, json, datetime, string

from pymongo import MongoClient

CHUNK_SIZE = 10000
DEFAULT_NUM_STUDENTS = 1000000

def main(argv):
    bearer_token = get_bearer_token()

    # number of students to create
    num_students = DEFAULT_NUM_STUDENTS

    # ids of existing institution entities in the database
    institution_ids = []
    grade_levels = []

    # default connection string
    connection = "mongodb://art:foo@ec2-34-208-44-30.us-west-2.compute.amazonaws.com:27017/art"

    output_format = "json"
    mode = "create"

    errors = False

    try:
        opts, args = getopt.getopt(argv, "hn:i:g:c:f:m:e:",
                                   ["help", "number=", "institutions=", "grades=", "connection=",
                                    "format=", "mode=", "errors="])
    except getopt.GetoptError:
        usage()
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
            sys.exit()
        elif opt in ("-n", "--number"):
            print "Number of students = " + arg
            num_students = int(arg)
        elif opt in ("-i", "--institutions"):
            print "Institutions = " + arg
            institution_ids = arg.split(',')
        elif opt in ("-c", "--connection"):
            print "Connection string = " + arg
            connection = arg
        elif opt in ("-g", "--grades"):
            print "Grades = " + arg
            grade_levels = arg.split(',')
        elif opt in ("-f", "--format"):
            print "Format = " + arg
            output_format = arg
        elif opt in ("-m", "--mode"):
            print "Mode = " + arg
            mode = arg
        elif opt in ("-e", "--errors"):
            print "Errors = " + arg
            errors = arg

    errors = (errors == "true" or errors == "True" or errors)

    institutions = get_institutions(connection, institution_ids)
    grade_levels = get_grade_levels(grade_levels)

    if output_format == "json" and mode == "create":
        # let's break up the creation of students into chunks to keep from killing
        # the API endpoint, which was never designed to handle 1,000,000 student inserts
        # at a time
        chunks, remainder = divmod(num_students, CHUNK_SIZE)
        print "\nGenerating %d chunks, %d remainder" % (chunks, remainder)

        print "\nStarting at: %s" % datetime.datetime.now()

        for chunk in range(0, chunks):
            print "\nGenerating and posting %d students..." % CHUNK_SIZE
            generate_and_post_student_data(CHUNK_SIZE, institutions, grade_levels, bearer_token)

        if remainder > 0:
            print "\nGenerating and posting %d students..." % remainder
            generate_and_post_student_data(remainder, institutions, grade_levels, bearer_token)

    else:
        print "Invalid format"


def generate_and_post_student_data(num_students, institutions, grade_levels, bearer_token):
    data = generate_student_data(num_students, institutions, grade_levels)
    post_student_batch_data(bearer_token, data)


def generate_student_data(num_students, institutions, grade_levels):
    data = []
    for i in range(0, num_students):
        data.append(create_student_dto(id_generator(), institutions, grade_levels))

    return data


def generate_data_file(data):
    print "Creating jsonStudents.txt at current directory"

    with open('jsonStudents.txt', 'w') as outfile:
        json.dump(data, outfile)


def get_bearer_token():
    endpoint = "https://sso-deployment.sbtds.org/auth/oauth2/access_token?realm=/sbac"
    headers = {"Content-Type" : "application/x-www-form-urlencoded"}

    payload = {
        "client_id": "pm",
        "client_secret" : "sbac12345",
        "grant_type" : "password",
        "password" : "password",
        "username" : "prime.user@example.com"
    }

    response = requests.post(endpoint, headers=headers, data=payload)
    content = json.loads(response.content)

    if response.status_code == 200:
        bearer_token = content["access_token"]
        print "Bearer token retrieved: %s" % bearer_token
        return bearer_token
    else:
        raise RuntimeError("Error retrieving SBAC access token")


def post_student_batch_data(bearer_token, data):
    endpoint = "https://art-capacity-test.sbtds.org/rest/external/student/CA/batch"
    headers = {"Content-Type": "application/json", "Authorization" : "Bearer %s" % bearer_token}

    response = requests.post(endpoint, headers=headers, data=json.dumps(data))

    if response.status_code == 202:
        location =  response.headers["Location"]
        print "Batch status URL: %s" % location
        return location
    else:
        print "Student API batch call failed with code: %d" % response.status_code
        return None


def create_student_dto(obj_id, institutions, grade_levels):
    institution_object = random_array_element(institutions)
    grade_level = random_array_element(grade_levels)

    race = [False, False, False, False, False, False]
    race[random.randint(0, 5)] = True

    day_separator = 1501

    return {
                "ssid": 'ASTDNT' + obj_id,
                "stateAbbreviation": "CA",
                "institutionIdentifier": institution_object['entityId'],
                "districtIdentifier": institution_object['parentEntityId'],
                "firstName": 'Name' + obj_id,
                "lastName": 'LastName' + obj_id,
                "middleName": 'MiddleName' + obj_id,
                "birthDate": datetime.date.fromordinal(
                    datetime.date.today().toordinal() - 1500 - random.randint(day_separator, 3000)).strftime("%F"),
                "externalSsid": 'STDNT' + obj_id,
                "gradeLevelWhenAssessed": grade_level,
                "sex": "Female" if random.randint(0, 1) == 0 else "Male",
                "hispanicOrLatino": race[0],
                "americanIndianOrAlaskaNative": race[1],
                "asian": race[2],
                "blackOrAfricanAmerican": race[3],
                "white": race[4],
                "nativeHawaiianOrPacificIsland": race[5],
                "twoOrMoreRaces": random_boolean(),
                "iDEAIndicator": random_boolean(),
                "lepStatus": random_boolean(),
                "section504Status": random_boolean(),
                "disadvantageStatus": random_boolean(),
                "languageCode": None,
                "migrantStatus": random_boolean(),
                "firstEntryDateIntoUsSchool": datetime.date.fromordinal(
                    datetime.date.today().toordinal() - random.randint(1, 1500)).strftime("%F"),
                "lepEntryDate": None,
                "lepExitDate": None,
                "title3ProgramType": None,
                "primaryDisabilityType": None,
                "elpLevel": 0
            }


def id_generator(size=7, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def random_boolean():
    if random.randint(0, 1) == 0:
        return False
    else:
        return True


def random_array_element(obj_array):
    return obj_array[random.randint(0, len(obj_array) - 1)]


def get_grade_levels(grade_levels):
    # default to grades 3-12 if none provided
    if len(grade_levels) == 0:
        grade_levels = range(3, 12)

    # clean up grade levels to make sure that they are 2 digits
    for idx, grade in enumerate(grade_levels):
        grade_levels[idx] = "{0:0>2}".format(grade_levels[idx])

    return grade_levels


def get_institutions(connection, institution_ids):
    try:
        client = MongoClient(connection)
        db = client.art

        # get the matching institutions objects
        if len(institution_ids) != 0:
            return list(db.institutionEntity.find({"entityId": {"$in": institution_ids}}))
        else:
            return list(db.institutionEntity.find({}))
    except:
        print "Unable to connect to ART mongodb to obtain institution/entity information."
        print "A seed file will still be generated, but will not be importable in ART."
        return []

def usage():
    print "Help/usage details:"
    print "  -c, --connection 	: mongo connection string (defaults to mongodb://localhost:27017/)"
    print "  -n, --number     	: the number of students to create"
    print "  --institutions   	: comma separated list of institution entityIds to use (from the institutionEntity collection). if none provided it will use all available"
    print "  --grades         	: comma separated list of grade levels to choose from. if none provided it will use 3-12"
    print "  -h, --help       	: this help screen"

main(sys.argv[1:])