from pymongo import MongoClient
import requests
from bs4 import BeautifulSoup

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
def update_v_1():
	print "Updating Succor"
	print "Generating email database"
	generate_email_table('emails.txt')
	print "Successfully generated email database"
	print "Generating smart search database"
	generate_smart_search_database('department_lists.csv')
	print "Successfully generated smart search database"
	print "Finished updating Succor"

###############################################################################
#                         END OF VERSION 1.0 UPDATES						  #
###############################################################################

###############################################################################
# 						 UPDATE TO SUPPORT VASSAR  							  #
###############################################################################
##
# Scrape Vassar course catalog and insert into departments database.
##
def scrape_vassar_course_cat():
	client = MongoClient()
	db = client.succor
	smart_search = db.smart_search

	# Get text as html
	html_doc = requests.get('https://secure3.vassar.edu/cgi-bin/geninfo.cgi').text
	soup = BeautifulSoup(html_doc)
	select_tag = soup.find('select', {'name' : 'dept'})

	for department in select_tag.select('option'):
		department_abbreviation = department.get('value')
		department_full_name = department.decode_contents(formatter="html")
		
		# Remove abbrevation from full name
		department_full_name = department_full_name.replace(department_abbreviation, "")
		# Replace special characters from full name
		department_full_name = department_full_name.replace("&amp;", "&")
		# Strip spaces from full name.
		department_full_name = department_full_name.strip()

		# Insert into database
		alternative_names_list = [department_abbreviation.lower(), department_full_name.replace(" ", "").lower()]

		smart_search.insert({
			'school' : 'vassar college',
			'department_name' : department_full_name,
			'alternative_names' : alternative_names_list
		})

	for department in smart_search.find({'school' : 'wesleyan university'}):
		smart_search.update(
			{'school' : 'vassar college', 
			'department_name' : department['department_name']},
			{'$pushAll' : 
				{
					'alternative_names' : department['alternative_names']
				}
			}
		)

scrape_vassar_course_cat()
###############################################################################
# 						 END UPDATE TO SUPPORT VASSAR  						  #
###############################################################################