import re

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
