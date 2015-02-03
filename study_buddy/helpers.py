from study_buddy import mail, Message, app, ts
from flask import url_for, render_template
from threading import Thread
from pymongo import MongoClient

import boto.ses
import re

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
	conn = boto.ses.connect_to_region(
		'us-west-2',
		aws_access_key_id=app.config['AWS_ACCESS_KEY_ID'],
		aws_secret_access_key=app.config['AWS_SECRET_KEY_ACCESS']
	)
	conn.send_email(
		app.config['FROM_EMAIL_ADDRESS'],
		"Vefiry your account with Succor",
		None,
		[email],
		text_body=render_template("email/verify.txt", url=confirm_url),
		html_body=render_template("email/verify.html", url=confirm_url)
	)
# 	send_email("Verify your account with Succor",
# 				app.config['ADMINS'][0],
# 				[email],
# 				render_template("email/verify.txt", url=confirm_url),
# 				render_template("email/verify.html", url=confirm_url))

# def send_async_email(app, msg):
# 	with app.app_context():
# 		print "Email sending..."
# 		mail.send(msg)
# 		print "Email sent!"

# def send_email(subject, sender, recipients, text_body, html_body):
# 	msg = Message(subject, sender=sender, recipients=recipients)
# 	msg.body = text_body
# 	msg.html = html_body
# 	thr = Thread(target=send_async_email, args=[app, msg])
# 	thr.start()
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
