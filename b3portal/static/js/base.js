function update(url, div) {
	$.post(url, function(data) {
		$("#" + div).before(data).remove();
	});
}
function do_call_get(url, id, hide) {
	$.get(url, function(data) {
		$("#"+id).html(data);
		if (hide) {
			$(hide).hide();
		}
	})
}
$(document).ready(
	function() {
		$('.option').each(
			function() {
				var b = $(this);
				var tt = b.text() || b.val();
				if ($(this).attr('type')) {
					b = $('<a>').insertAfter(this).addClass(
							this.className).attr('id', this.id);
					if ($(this).attr('type')=='submit') {
						b.attr('alt','submit');
					}
					if (this.name) {
						$(this).before('<input type="hidden" value="true" name="'+this.name+'"/>');
					}
					$(this).remove();
				}
				b.text('').css( {
					cursor :'pointer'
				}).prepend('<i></i>').append(
						$('<span>').text(tt).append(
								'<i></i><span></span>'));
			});
		$("a[alt='submit']").click( function(){
			form = $(this).parent("form");
			form.submit();
		});
		$("form.default input").each(
			function() {
				$(this).keypress(function (e) {
					if ((e.which && e.which == 13) || (e.keyCode && e.keyCode == 13)) {
						form = $(this).parents("form");
						form[0].submit();
						return false;
					} else {
						return true;
					}
				});  
			}	
		);
	    $('ul.messages li').each(function() {
	        $(this).append("<img class='close_button' src='"+MEDIA_URL+"/images/close.gif'/>");
	     });
	     $('.close_button').click(function() {
	         $(this).parent().remove();
	     })
	}
);

