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
function do_get(url, elem) {
	$.get(url, function(data) {
		$(elem).html(data);
	})
}
function update_user_messages(callback) {
	$.get(MUP_URL, function(data) {
		$("#message_teaser").html(data);
		if (callback) callback();
	})	
}

function isEmpty(ob){
    for(var i in ob){ return false;}
	return true;
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
		/*$("a[alt='link']").ajaxlink({success: 'main_content'});*/
	    /*$('ul.messages').on('show','li', function() {
	        $(this).append("<img class='close_button' src='"+MEDIA_URL+"images/close.gif'/>");
	     });
	     $('.close_button').click(function() {
	         $(this).parent().remove();
	     })*/
	}
);
$(document).ajaxSend(function(event, xhr, settings) {
/*    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }*/
    function sameOrigin(url) {
        // url could be relative or scheme relative or absolute
        var host = document.location.host; // host + port
        var protocol = document.location.protocol;
        var sr_origin = '//' + host;
        var origin = protocol + sr_origin;
        // Allow absolute or scheme relative URLs to same origin
        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            // or any other URL that isn't scheme relative or absolute i.e relative.
            !(/^(\/\/|http:|https:).*/.test(url));
    }
    function safeMethod(method) {
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    if (!safeMethod(settings.type) && sameOrigin(settings.url)) {
        xhr.setRequestHeader("X-CSRFToken", $.cookie('csrftoken'));
    }
});
