function addUpload() {

/*	
	var num = 'nu' + $("#uploads").children().length;

	var new_upload = "<p>Upload prompt:<textarea id='upload_prompt_"+num+"' name='upload_prompt_"+num+"' class='upload_prompt_field' rows='3'></textarea></p>";

	$("#uploads").append(new_upload);
	$('#upload_prompt_' + num).focus();
*/

}

function addQuestion() {
	
	var num = $("#questions").children().length;
	
	var new_q = $("new_question .ui-dialog").clone();
	
	//for each child(-r) in new_q with class = "interactive", append Num to its ID
	//for each child(-r) in new_q of type "input" or "textarea", append Num to its name
	
	//append new_q to the list
	$("#questions").append(new_q);
	
	//focus new_q
	$('#question_prompt_new' + num).focus();
}