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
    
var autocomplete_data = [];

$(document).ready(function(){
	$('#page-header').fadeIn(1500);
    $('.click').click(function(e){
        var id = $(e.currentTarget).data('id');
        var id2='.container[data-id=' + id + ']';
        if($(id2).hasClass('hidden')){
        $(id2).slideDown();
        $(id2).addClass('shown');
        $(id2).removeClass('hidden');
    }
    else {
    	$(id2).slideUp();
        $(id2).addClass('hidden');
        $(id2).removeClass('shown');
    }
    });

    // Preprocessing departments list.
    for (i in data) {
        var name_json = {};
        var short_name = data[i][0];
        var long_name = data[i][1];
        name_json["label"] = short_name+"-"+long_name;
        autocomplete_data.push(name_json);
    }

    $("#studysearch").autocomplete({
        source: autocomplete_data
    });
});

