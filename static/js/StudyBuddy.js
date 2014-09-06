// JSON tags
var CLASS_NAME_TAG = "";
var TIME_TAG = "";
var ASSIGNMENT_TAG = "";
var STUDY_PARTNER_TAG = "";
var LOCATION_TAG = "";

// Base url for site
var BASE_URL = "";

//Code that runs right after window has loaded
window.onload = function() {
	//code that runs when you click the search button
	document.getElementById("find").onclick = function(){
		console.log("error");
		var keyword = document.getElementById("studysearch").value;
		window.location = "/find?search_keyword="+keyword;

	}
	document.getElementById("create").onclick = function(){
		window.location = "/create"

	}
	document.getElementById("lucky").onclick = function(){
		window.location = "/lucky"
	}
}



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


