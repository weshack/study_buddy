'''
ogArray is an array of 2-element arrays
containing the acronym and full name of
all academic departments at Wesleyan.

'''

def validDept(rawName):
	combined_list = combineShortAndLong(depts)
	if rawName in combined_list:
		return True
	print "FUCK NOOOOOOOOOOOOOOOOOOOOOOO"
	return False

def combineShortAndLong(depts_list):
	combined_list = []
	for dept in depts_list:
		short_name = dept[0]
		long_name = dept[1]
		combined_list.append(short_name.lower() + "-" + long_name.lower())
		print combined_list
	return combined_list

##
# This function will return the department full and short name that most closely
# matches the search term, within reasonable limits.
##
def matchSearchTerm(search_term):
	if search_term not in combineShortAndLong(depts):
		for pair in depts:
			if search_term.upper() == pair[0] or search_term.upper() == pair[1].upper():
				return pair[0] + "-" + pair[1]
				break
	return search_term



depts = [["AFAM","African American Studies Program"],
["AMST", "American Studies"],
["ANTH", "Anthropology"],
["ARAB", "Arabic"],
["ARCP", "Archaeology Program"],
["ARHA", "Art History"],
["ARST", "Art Studio"],
["ASTR", "Astronomy"],
["BIOL", "Biology"],
["CCIV", "Classical Civilization"],
["CEAS", "College of East Asian Studies"],
["CHEM", "Chemistry"],
["CHIN", "Chinese"],
["CHUM", "Center for the Humanities"],
["CIS", "College of Integrative Sciences"],
["COL", "College of Letters"],
["COMP", "Computer Science"],
["CSPL", "Center for the Study of Public Life"],
["CSS", "College of Social Studies"],
["DANC", "Dance"],
["E&ES", "Earth and Environmental Sciences"],
["ECON", "Economics"],
["ENGL", "English"],
["ENVS", "Environmental Studies Program"],
["FGSS", "Feminist, Gender, and Sexuality Studies Program"],
["FILM", "Film Studies"],
["FIST", "French, Italian, Spanish in Translation"],
["FREN", "French"],
["FRST", "French Studies"],
["GELT", "German Literature in English"],
["GOVT", "Government"],
["GRK", "Greek"],
["GRST", "German Studies"],
["HEBR", "Hebrew"],
["HEST", "Hebrew Studies"],
["HIST", "History"],
["ITAL", "Italian Studies"],
["JAPN", "Japanese"],
["KREA", "Korean"],
["LANG", "Less Commonly Taught Languages"],
["LAST", "Latin American Studies Program"],
["LAT", "Latin"],
["MATH", "Mathematics"],
["MB&B", "Molecular Biology and Biochemistry"],
["MDST", "Medieval Studies Program"],
["MUSC", "Music"],
["NS&B", "Neuroscience and Behavior"],
["PHED", "Physical Education"],
["PHIL", "Philosophy"],
["PHYS", "Physics"],
["PORT", "Portuguese"],
["PSYC", "Psychology"],
["QAC", "Quantitative Analysis Center"],
["REES", "Russian, East European, and Eurasian Studies Program"],
["RELI", "Religion"],
["RULE", "Russian Literature in English"],
["RUSS", "Russian"],
["SISP", "Science in Society Program"],
["SOC", "Sociology"],
["SPAN", "Spanish"],
["THEA", "Theater"],
["WRCT", "Writing Center"]]

