var data = 
    [["AFAM", "African American Studies Program"],
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

    $('.edit-button').click(function(e) {
            var id = $(this).attr('id');
            table_row = $('[data-id="' + id + '"]');
        //targetId = e.currentTarget.attr('id');
        if ($(this).hasClass('edit-button')) {
            $(this).text('Done');
            $(this).addClass('done-button');
            $(this).removeClass('edit-button');
            // change fields to inputs.
             console.log(table_row);
             var time= $(table_row[1]).text();
             $(table_row[1]).replaceWith("<td><input id='"+id+"-time' type='text' value='" + time + "'></td>");
             var location= $(table_row[2]).text();
             $(table_row[2]).replaceWith("<td><input id='"+id+"-location' type='text' value='" + location + "'></td>");
             var description= $(table_row[3]).text();
             $(table_row[3]).replaceWith("<td><input type='text' id='"+id+"-description' value='" + description + "'></td>");

             var text= $($($(table_row[4]).children()[1]).children()[2]).text();
            console.log(text);
             $($($(table_row[4]).children()[1]).children()[2]).replaceWith("<input type='text' id='"+id+"-session_details' value='" + text + "'>");

        } else {
            
            console.log(table_row);
            $(this).text('Edit');
            $(this).addClass('edit-button');
            $(this).removeClass('done-button');
            var time=document.getElementById(id+"-time").value;
            var location=document.getElementById(id+"-location").value;
            var description=document.getElementById(id+"-description").value;
            var session_details=document.getElementById(id+"-session_details").value;
            console.log(time,location,description,session_details);
            //send ajax request to /edit.
            $.ajax({
                method: 'POST',
                data: {
                   time : time,
                   location:location,
                   description:description,
                   session_details:session_details,
                },
                url: '/edit?group_id=' + id,
                success: function(result) {
                    console.log(result);
                    // $(table_row[1]).replaceWith("<td class='click' data-id=id>"+time+"</td>");
                    // $(table_row[2]).replaceWith("<td class='click' data-id=id>location</td>");
                    // $(table_row[3]).replaceWith("<td style='overflow:auto' class='click' data-id=id>description</td>");
                    // $($($(table_row[4]).children()[1]).children()[2]).replaceWith("<p id=id>"+session_details+"</p>");
                    
                    // change back fields
                }
    });
        }
    });


});

function onAddUserButtonClick(groupID, userID) {
    console.log("pressed add user button");
    console.log("groupID: " + groupID + " userID: " + userID);

    $.ajax({
        method: 'POST',
        url: '/join?group_id=' + groupID,
        success: function(result) {
            console.log(result);
            // remove button

            // add name to table
        }
    });
}

