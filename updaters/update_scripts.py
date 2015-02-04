from pymongo import MongoClient

###############################################################################
# 							Update to version 1.0 							  #
###############################################################################
# generate_email_table: generates lookup table matching
# email addresses to school names.
#
# generate_smart_search_database: generate database matching
# common names of departments to a single standardized name
# used in searches and in creating study groups.
##
def generate_email_table(filename):
	client = MongoClient()
	db = client.succor
	schools = db.schools

	f = open(filename, 'r')
	for line in f:
		email = line.split(':')[0].strip()
		school = line.split(':')[1].strip()
		schools.insert({'email' : email, 'school' : school, 'users' : 0})

def generate_smart_search_database(filename):
	client = MongoClient()
	db = client.succor
	smart_search = db.smart_search

	f = open(filename, 'r')

	for line in f.read().split('\r'):
		line_list = line.split(",")
		department = line_list[0]
		alternative_names = line_list[1]
		alternative_names_list = alternative_names.split(";")
		alternative_names_list.append(department)
		alternative_names_list_processed = [name.replace(" ", "").lower() for name in alternative_names_list]
		school_name = "wesleyan university"
		smart_search.insert(
			{'school' : school_name,
			 'department_name' : department,
			 'alternative_names' : alternative_names_list_processed
			 })

print "Updating Succor"
# print "Generating email database"
# generate_email_table('emails.txt')
# print "Successfully generated email database"
print "Generating smart search database"
generate_smart_search_database('department_lists.csv')
print "Successfully generated smart search database"
print "Finished updating Succor"

###############################################################################
#                         END OF VERSION 1.0 UPDATES						  #
###############################################################################