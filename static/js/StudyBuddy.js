// JSON tags
var CLASS_NAME_TAG = "";
var TIME_TAG = "";
var ASSIGNMENT_TAG = "";
var STUDY_PARTNER_TAG = "";
var LOCATION_TAG = "";

// Base url for site
var BASE_URL = "";

var autocomplete_data = [];

//Code that runs right after window has loaded
window.onload = function() {
	//code that runs when you click the search button
	document.getElementById("find").onclick = function(){
		var keyword = document.getElementById("studysearch").value;
		var course_no = document.getElementById("course-search").value;
		window.location = "/find?search_keyword="+keyword+"&course_no="+course_no;
	}	
	document.getElementById("create").onclick = function(){
		window.location = "/create"

	}
	document.getElementById("lucky").onclick = function(){
		window.location = "/lucky"
	}

	var data = 
	[["AMST", "American Studies"],
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
	["WRCT", "Writing Center"]];

	for (i in data) {
		var name_json = {};
		var short_name = data[i][0];
		console.log(short_name);
		var long_name = data[i][1];
		console.log(long_name);
		name_json["label"] = short_name+"-"+long_name;
		autocomplete_data.push(name_json);
	}	

	$("#studysearch").autocomplete({
		source: autocomplete_data
	});

	window.onresize = function() {
		var input_size = document.getElementById("studysearch").style.width;
		document.getElementsByClass("ui-widget-content")[0].style.width = input_size;
	}

};


function parseJson(json) {
	var obj = JSON.parse(json);
	for (item in obj) {
		var className = item[CLASS_NAME_TAG];
		var assignment_name = item[ASSIGNMENT_TAG];
		var time_of_meeting = item[TIME_TAG];
		var study_location = item[LOCATION_TAG];
		var list_of_partners = item[STUDY_PARTNER_TAG];

	}
	
}

// Return data in json form from url.
function queryURL(url) {
	var requestURL = BASE_URL + url;
	var request = new XMLHttpRequest();

	request.open("get", requestURL, true);

	request.onreadystatechange = function() {
		if (request.readyState != 4) {
			return;
		}

		return request.responseText;
	}

	request.send();
}

$(function() {
	$( "#datepicker" ).datepicker();
  });

