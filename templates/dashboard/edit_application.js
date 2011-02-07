function set_click_handlers() {
}

function addUpload() {

	var num = 'nu' + $("#uploads").children().length;

	var new_upload = "<p>Upload prompt:<textarea id='old_upload_prompt_new'+num+' name='old_upload_prompt_new_"+num+" class='upload_prompt_field' rows='3'></textarea></p>";

	$("#uploads").append(new_upload);
	$('#upload_prompt_' + num).focus();

}

function addQuestion() {

	//an arbitrary integer that's unique among the newly added Qs
	var num = $("#questions").children().length + 1;
	
	var new_q = $("#new_question > div").clone();
	var new_id = 'new_question_' + num;
	
	new_q.attr('id', new_id);
	new_id = '#' + new_id;
	
	//append new_q to the list
	$("#questions").append(new_q);

	//set title
	$(new_id + " h4").html("Question #" + num);
	
	//unique IDs to support hiding & showing sections
	$(new_id + " .interactive, " + new_id + " :checkbox").each(function() {		
		$(this).attr('id', $(this).attr('id') + num);
	});
	
	//ensure labels remain attached to the correct checkbox
	$(new_id + " label").each(function() {
		$(this).attr('for', $(this).attr('for') + num);
	});
	
	//for each child(-r) in new_q of type "input" or "textarea", append Num to its name
	$(new_id + " input, " + new_id + " textarea").each(function () {
		$(this).attr('name', $(this).attr('name') + num);
		$(this).attr('id', $(this).attr('id') + num);
	});

    $("#answer_choices_new" + num).click(function() { 
            $('#choices_div_new' + num).slideDown();
            $('#choices_new' + num).focus(); 
         });
    $("#answer_choices_new" + num).attr("onclick", "");
		
    $("#answer_text_new" + num).click(function() { 
            $('#choices_div_new' + num).slideUp();
         });
    $("#answer_text_new" + num).attr("onclick", "");

	//focus new_q
	$('#question_prompt_new' + num).focus();

	set_click_handlers();
	
}
