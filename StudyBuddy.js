// JSON tags
var CLASS_NAME_TAG = "";
var TIME_TAG = "";
var ASSIGNMENT_TAG = "";
var STUDY_PARTNER_TAG = "";
var LOCATION_TAG = "";

// Base url for site
var BASE_URL = "";


window.onload = function() {
	//code that runs when you click the search button
	document.getElementById("search").submit=function(){
		var keyword = document.getElementById("studysearch")[0].value;
		var jsondata = queryURL("/search/"+keyword);

	}
}

function parseJson(json) {
	var obj = JSON.parse(json);

	var className = obj[CLASS_NAME_TAG];
	var assignment_name = obj[ASSIGNMENT_TAG];
	var time_of_meeting = obj[TIME_TAG];
	var study_location = obj[LOCATION_TAG];
	var list_of_partners = obj[STUDY_PARTNER_TAG];	
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


