function set_indicator_position() {
	if ($(".nav-active").length != 0) {
		$("#nav-active-indicator").offset({top: $(".nav-active").offset().top + ($(".nav-active").height() * .15) });
		$("#nav-active-indicator").show();
	}
};
$(document).ready(function() {
    set_indicator_position();
/*    $(".nav-button").click(function() {
        if (!$(this).hasClass("nav-active")) {
            $(".nav-active").removeClass("nav-active");
            $(this).addClass("nav-active");
            set_indicator_position();
        }
    });*/
    $("#profile .avatar").click(function(e) {
        $("#profile-box").toggle();
        e.stopPropagation();
    });
    $(document).click(function(e) {
    	var container = $("#profile-box");
	    if (container.has(e.target).length === 0) {
	        container.hide();
	    }
    });
})