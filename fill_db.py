import departmentArray
import string
import random

from pymongo import MongoClient
client = MongoClient()

db = client.sbdb

DEPARTMENT_KEY = "department"
COURSE_NUMBER_KEY = "course_no"
LOCATION_KEY = "location"
TIME_KEY = "time"
COURSE_NOTES_KEY = "course_notes"
CONTACT_KEY = "contact"
DESCRIPTION_KEY = "description"
OWNER_NAME_KEY = "owner"
OWNER_ID_KEY = "owner_id"




# clear db
db.drop_collection('users')
db.drop_collection('group_sessions')

# get collections we want
users = db.users
group_sessions = db.group_sessions


NUM_USERS = 40
NUM_GROUPS = 20

class RandomUser:
	def __init__(self):
		self.id = str(random.randint(10000, 99999)) 
		self.name = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))

class RandomGroup:
	def __init__(self):
		self.department = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))
		self.course_no = str(random.randint(100, 999)) 
		self.location = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))
		self.time = str(random.randint(10000, 99999)) 
		self.course_notes = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(100))
		self.description = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(50))
		self.contact = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))
		self.ownerID = None
		self.ownerName = None


def addRandomUsers():
	for i in range(NUM_USERS):
		user = RandomUser()
		db.users.insert({"id":user.id,"name":user.name})

def addRandomGroup():
	#Creates random group, pulls a random user, adds user as owner of group
	users = db.users.find()
	group = RandomGroup()
	for i in range(NUM_GROUPS):
		randUser = users[random.randint(0,NUM_USERS-1)]
		new_group = {
				DEPARTMENT_KEY    : group.department,
                COURSE_NUMBER_KEY : group.course_no,
                LOCATION_KEY      : group.location,
                TIME_KEY          : group.time,
                COURSE_NOTES_KEY  : group.course_notes,
                CONTACT_KEY       : group.contact,
                DESCRIPTION_KEY   : group.description,
                OWNER_NAME_KEY 	  : randUser['name'],
                OWNER_ID_KEY      : randUser['id']
            }
		db.group_sessions.insert(new_group)


addRandomUsers()
addRandomGroup()