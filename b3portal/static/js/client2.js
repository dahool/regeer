function create_dialog(id, callback) {
    $(id).click(function() {
        var dialog = $('<div id="content_dialog" style="display:none; text-align: left;"></div>').appendTo('body');
        var url = $(this).attr('alt');
        dialog.load(
            url, 
            function (responseText, textStatus, XMLHttpRequest) {
                dialog.dialog({
                    modal: true,
                    width: 550,
                    close: function(event, ui) {
                        dialog.remove();
                    }
                });
            }
        );
        dialog.on('submit','form', function(ev) {
            ev.preventDefault();
            $.post($(this).attr('action'),
                    $(this).serializeArray(),
                    function(data, status, xr) {
                        if (typeof(data) === "string") {
                            $("#content_dialog").html(data);
                        } else {
                            $(ev.delegateTarget).dialog('close');
                            update_user_messages(function() { callback(data); });
                        }
                    }
            );
        });
    }); 
}
$(document).ready(
	function() {
		$(".clientPanelTabContent div:first").show();
		$(".clientPanelTabGroup li").click(function() {
			var tabId = $(this).attr('alt');
			$('.clientPanelTabContent .clientContentTab:not(#'+tabId+')').hide();
			$('#'+tabId).show();
			$('.clientPanelTabGroup li:not(alt['+tabId+'])').removeClass('tab_selected');
			$(this).addClass('tab_selected');
		});
		
		// ajax boxes
		$('#client_aliases').on('click','div.pagination a', function(e) {
			e.preventDefault();
			do_get($(this).attr('href'),$('#client_aliases'));
		});
		$('#client_ipaliases').on('click','div.pagination a', function(e) {
			e.preventDefault();
			do_get($(this).attr('href'),$('#client_ipaliases'));
		});	
		$('#client_notice').on('click','div.pagination a', function(e) {
			e.preventDefault();
			do_get($(this).attr('href'),$('#client_notice'));
		});		
		$('#past_penalties').on('click','div.pagination a', function(e) {
			e.preventDefault();
			do_get($(this).attr('href'),$('#past_penalties'));
		});			
		$('#admin_actions').on('click','div.pagination a', function(e) {
			e.preventDefault();
			do_get($(this).attr('href'),$('#admin_actions'));
		});
		$('#portal_actions').on('click','div.pagination a', function(e) {
			e.preventDefault();
			do_get($(this).attr('href'),$('#portal_actions'));
		});
		$('#player_actions').on('click','div.pagination a', function(e) {
			e.preventDefault();
			do_get($(this).attr('href'),$('#player_actions'));
		});		
		$('#admin_log_actions').on('click','div.pagination a', function(e) {
			e.preventDefault();
			do_get($(this).attr('href'),$('#admin_log_actions'));
		});		
	}
);