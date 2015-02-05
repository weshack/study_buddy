from study_buddy import app, ts
from flask import url_for, render_template
from pymongo import MongoClient
from json import dumps

import boto.ses
import re

##
# Given a wtf form object, return a json representation of the data 
# in that form.
#
# @param form WTF form object
#
# @return Returns a JSON representation of the data in form
##
def json_from_form(form):
	form_dict = {}
	for field_name, value, in form.data.items():
		form_dict[field_name] = value
	return form_dict

##
# Given a search term for a department, determines what the user
# meant to search for.
#
# @param search_term The user-input search term.
# @param school The school in which we are searching for a department.
#
# @return Returns the term most closely matching the term the user input.
##
def smart_search(search_term, school):
	client = MongoClient()
	conn = client.succor.smart_search
	search_term_processed = search_term.replace(" ", "").lower()
	if school: 
		school = school.lower()
		result = conn.find_one(
			{'school' : school, 
			 'alternative_names' : {'$in' : [search_term_processed]}}
		)
	else:
		result = conn.find_one(
			{'alternative_names' : {'$in' : [search_term_processed]}}
		)
	print "search term:", search_term
	print "school:", school
	
	print "smart search result:", result
	if result:
		return result['department_name']
	else:
		return search_term

##
# Finds the school name based on the email domain name given.
#
# @param email_ending The email domain name of the users email address.
#
# @return Returns the school name based on the email address given.
##
def school_name_from_email(email_ending):
	client = MongoClient()
	conn = client.succor.schools
	result = conn.find_one({'email' : email_ending})
	if result:
		return result['school']
	else:
		return email_ending

##
# Sends an email to a user who has just registered, with
# with instructions on how to verify account.
#
# @param unique_id Unique ID that will be used to identify user in URL.
# @param email Email address to send verification link to.
##
def send_verification_email(email):
	token = ts.dumps(email, salt='email-confirm-key')
	confirm_url = url_for('verify', token=token, _external=True)
	send_email(
		"Vefiry your account with Succor",
		app.config['FROM_EMAIL_ADDRESS'],
		[email],
		render_template("email/verify.txt", url=confirm_url),
		render_template("email/verify.html", url=confirm_url)
	)

def send_email(subject, sender, recipients, text_body, html_body):
	conn = boto.ses.connect_to_region(
		'us-west-2',
		aws_access_key_id=app.config['AWS_ACCESS_KEY_ID'],
		aws_secret_access_key=app.config['AWS_SECRET_KEY_ACCESS']
	)

	conn.send_email(
		sender,
		subject,
		None,
		recipients,
		text_body=text_body,
		html_body=html_body
	)

##
# @returns returns True if c is a number
##
def is_number(c):
	try:
		float(c)
		return True
	except ValueError:
		return False

##
# Given a string, query, this function parses it to find a
# department and a course number and returns a tuple of the two.
# @returns return (department : string, course_number : string)
##
def parse_new_find(query):
	is_digit = False
	department_end = -1
	number_end = -1
	for i in range(1, len(query)+1):
		c = query[len(query) - i]
		if is_number(c) and is_digit:
			continue
		if is_number(c):
			is_digit = True
			number_end = (len(query) + 1) - i
		if not is_number(c):
			is_digit = False
			department_end = (len(query) + 1) - i
			break

	if department_end >= 0 and number_end >= 0:
		course_number = query[department_end : number_end]
		department_name = query[0 : department_end]
	elif department_end >= 0:
		department_name = query[0 : department_end]
		course_number = ''
	else:
		department_name = ''
		course_number = ''

	print query
	print "course number:", course_number
	print "department name:", department_name
	print "================================================="

	return (department_name.strip(), course_number.strip())
