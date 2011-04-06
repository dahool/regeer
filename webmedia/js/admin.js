function getCurrentTime() {
	var d = new Date();
	return d.format("HH:MM:ss");
}
function value_do(name, value) {
	$('input[name='+name+']').val(value);
	$('input[alt='+name+']').click();
}
function send_command(cmd, action) {
	d = $('[name='+cmd+']');
	if (d) {
		data = d.val();
	} else {
		data = 'None';
	}						
	$.post(POST_URL, {cmd: cmd, data: data, action: action}, function(data) {
		$('#response').prepend(getCurrentTime() + " - " + data + "<br/>");
	});
}
$(document).ready(
	function() {
		$('.command_get').each(
			function() {
				$(this).click(
					function() {
						n = $(this).attr('alt');
						send_command(n, 'get');
					}
				);
			}
		);
		$('.command_set').each(
				function() {
					$(this).click(
							function() {
								n = $(this).attr('alt');
								send_command(n, 'set');
							}
						);
				}
			);
	}
);