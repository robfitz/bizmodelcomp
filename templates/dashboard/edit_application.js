function set_click_handlers() {
	
	$('.show_choices').click( function() {

		var id = get_id($(this));

		if ( $( this ).attr( "checked" ) ) {
			$( "#choices_div_" + id ).slideDown();
		}
		else {
			$( "#choices_div_" + id ).slideUp();
			//$( "#choices_div_" + id + " textarea" ).text("");
		}
	});

	$('.has_score').click( function() {

		var id = get_id( $(this) );

		if ( $( this ).attr( "checked" ) ) {
			$( "#score_div_" + id ).slideDown();
			var curr_score = $( "#score_div_" + id + " .max_points").val();
			if (parseInt(curr_score) == 0) {
				$( "#score_div_" + id + " .max_points").val(10);
			}
		}
		else {
			$( "#score_div_" + id ).slideUp();
			//$( "#score_div_" + id + " .max_points").val(0);
			//$( "#score_div_" + id + " .points_prompt").text("");

		}
	});

	$('.has_feedback').click( function() {

		var id = get_id( $(this) );

		if ( $( this ).attr( "checked" ) ) {
			$( "#feedback_div_" + id ).slideDown();
		}
		else {
			$( "#feedback_div_" + id ).slideUp();
			//$( "#feedback_div_" + id + " textarea").text("");
		}
	});
	
	$('.is_judge_only').click( function() {
	
		var id = get_id( $(this) );
		
		if ( $(this).attr( "checked" ) ) {
			$("#applicant_prompt_" + id).slideUp();
		}
		else {
			$("#applicant_prompt_" + id).slideDown();
		}
	
	});
}

function addUpload() {

/*	
	var num = 'nu' + $("#uploads").children().length;

	var new_upload = "<p>Upload prompt:<textarea id='upload_prompt_"+num+"' name='upload_prompt_"+num+"' class='upload_prompt_field' rows='3'></textarea></p>";

	$("#uploads").append(new_upload);
	$('#upload_prompt_' + num).focus();
*/

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
	$(new_id + " .section_title").html("Question #" + num);
	
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
	});
		
	//focus new_q
	$('#question_prompt_new' + num).focus();

	set_click_handlers();
	
}