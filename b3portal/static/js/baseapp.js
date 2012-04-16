$(document).ready(function() {
	$(".notice_tip").tipTip({delay: 200, defaultPosition: 'left'});
	$("#quick_server").on('change', function() {
		$("#server_search_quick").val($(this).val());
	});	
});
