from pymongo import MongoClient

client = MongoClient()
db = client.succor
schools = db.schools

f = open('emails.txt', 'r')
for line in f:
	email = line.split(':')[0].strip()
	school = line.split(':')[1].strip()
	schools.insert({'email' : email, 'school' : school, 'users' : 0})