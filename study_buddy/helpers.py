from study_buddy import mail, Message, app, ts
from flask import url_for, render_template
from threading import Thread
import re

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
	send_email("Verify your account with Succor",
				app.config['ADMINS'][0],
				[email],
				render_template("email/verify.txt", url=confirm_url),
				render_template("email/verify.html", url=confirm_url))

def send_async_email(app, msg):
	with app.app_context():
		mail.send(msg)

def send_email(subject, sender, recipients, text_body, html_body):
	msg = Message(subject, sender=sender, recipients=recipients)
	msg.body = text_body
	msg.html = html_body
	thr = Thread(target=send_async_email, args=[app, msg])
	thr.start()
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
