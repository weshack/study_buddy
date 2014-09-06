'''
ogArray is an array of 2-element arrays
containing the acronym and full name of
all academic departments at Wesleyan.

'''

def validDept(rawName,depts):
	for name in depts:
		if name[0] == rawName or name[1] == rawName:
			print "FUCK YEAAAAHHHHHH"
			return True
	print "FUCK NOOOOOOOOOOOOOOOOOOOOOOO"
	return False

depts = [["AMST", "American Studies"],
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

