$(document).ready(function() {
	$(".topbar-content").width($(".topbar").width()-$(".topbar-button-close-container").width()-10);
	$(".topbar-button-close").click(function() {
	  	$(".topbar-container").slideUp('fast', function() {
	  		$(".topbar-button-open-container").slideDown('fast');
	  		$.cookie('topbar_status', 'closed', { expires: 365, path: '/' });
		});
	})
	$(".topbar-button-open").click(function() {
		$(".topbar-button-open-container").slideUp('fast', function() {
			$(".topbar-container").slideDown('fast');
			$.cookie('topbar_status', 'open', { expires: 365, path: '/' });
		});
	})
	if ($.cookie('topbar_status') == "open") {
		$(".topbar-container").show();
	} else {
		$(".topbar-button-open-container").show();
	}
}); 