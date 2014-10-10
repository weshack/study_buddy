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
//MUST HAVING SOMETHING TO TRIGGER IT SO IT CAN ACTIVATE
window.onload = function() {
    $('#datetimepicker').datetimepicker({
        allowTimes:[
        '24:00','24:30','1:00','1:30','2:00','2:30','3:00','3:30','4:00','4:30','5:00','5:30','6:00','6:30',
        '7:00','7:30','8:00','8:30','9:00','9:30','10:00','10:30','11:00','11:30','12:00','12:30',
        '13:00','13:30','14:00','14:30','15:30','16:00','16:30','17:00','17:30','18:00','18:30',
        '19:00','19:30','20:00','20:30','21:00','21:30','22:00','22:30','23:00','23:30'
        ]
        });
    var data =
        [
            ["AFAM","African American Studies Program"],
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
            ["WRCT", "Writing Center"]
        ];

    for (i in data) {
        var name_json = {};
        var short_name = data[i][0];
        console.log(short_name);
        var long_name = data[i][1];
        console.log(long_name);
        name_json["label"] = short_name+"-"+long_name;
        autocomplete_data.push(name_json);
    }   

    $("#createdepartment").autocomplete({
        source: autocomplete_data
    });



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





