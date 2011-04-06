function control_checkbox(elem) {
	if ($(elem).attr('checked')) {
		$("label[for=id_time]").hide();
		$("label[for=id_time_type]").hide();
		$("#id_time").hide();
		$("#id_time_type").hide();
	} else {
		$("label[for=id_time]").show();
		$("label[for=id_time_type]").show();		
		$("#id_time").show();
		$("#id_time_type").show();
	}
}
function register_user(url, value) {
	$.post(url, {'value': value}, function(data) {
		$('#client_group').html(data);
		$('#client_group').attr('class','');
		$('#client_group').attr('onclick','');
	});	
}
$(document).ready(
	function() {
		$('[name=autofill]').each(
				function() {
					$(this).css('cursor','pointer');
					$(this).click(function(){
						name = $(this).attr('alt');
						$('select[name=type] option').each(
							function() {
								if ($(this).attr('value')==name) {
									$(this).attr('selected','selected');
								}
							}
						);
						$('#data').val($(this).text());
					})
				}
		);
		$('[class=autofill2]').each(
				function() {
					$(this).css('cursor','pointer');
					$(this).click(function(){
						name = $(this).attr('name');
						value = $(this).attr('alt');
						$('#'+name).val(value);
					})
				}
		);		
		$('#id_permanent').change(function() {
			control_checkbox($(this));	
		});
		$('#id_permanent:checked').each(function() {
			control_checkbox($(this));	
		});
	}
);