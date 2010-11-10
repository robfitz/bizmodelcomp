function addUpload() {

	var num = $("#uploads").children().length

	var new_upload = "<p>Upload prompt:<textarea id='upload_prompt_"+num+"' name='upload_prompt_"+num+"' class='upload_prompt_field' rows='3'></textarea></p>";

	$("#uploads").append(new_upload);
	$('#upload_prompt_' + num).focus();
}

function addQuestion() {
	var num = $("#questions").children().length

	var new_upload = "<p>Question prompt:<textarea id='question_prompt_"+num+"' name='question_prompt_"+num+"' class='question_prompt_field' rows='3'></textarea></p>";

	$("#questions").append(new_upload);
	$('#question_prompt_' + num).focus();
}