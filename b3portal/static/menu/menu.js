$(document).ready(function(){
	$("ul.subnav").parent().append('<span class="sub"></span>');
	
	$("ul.subnav").parent().find("a").each(function() {
		if ($(this).attr("alt")=="span") {
			$(this).click(function() {
				$(this).parent().find("span.sub").click();
			});
		}
	});
	
	$("span.sub").each(function() {
    	
	    $(this).click(function() { //When trigger is clicked...

	        //Following events are applied to the subnav itself (moving subnav up and down)
	        $(this).parent().find("ul.subnav").slideDown('fast').show(); //Drop down the subnav on click

	        $(this).parent().hover(function() {
	        }, function(){
	            //$(this).parent().find("ul.subnav").slideUp('slow'); //When the mouse hovers out of the subnav, move it back up
	        	$(this).parent().find("ul.subnav").fadeOut('slow'); //When the mouse hovers out of the subnav, move it back up
	        });

	        //Following events are applied to the trigger (Hover events for the trigger)
	        }).hover(function() {
	            $(this).addClass("subhover"); //On hover over, add class "subhover"
	        }, function(){  //On Hover Out
	        	$(this).removeClass("subhover"); //On hover out, remove class "subhover"
	    });
    	
    	
    });
    

});
