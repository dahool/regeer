$(document).ready(function(){
    $("ul.subnav").parent().append('<span class="sub"></span>');

    $("ul.subnav").parent().hover(function() { //When trigger is clicked...
        $(this).find("span.sub").addClass("subhover"); //On hover over, add class "subhover"

        //Following events are applied to the subnav itself (moving subnav up and down)
        $(this).find("ul.subnav").slideDown('fast').show(); //Drop down the subnav on click

        $(this).hover(function() {
        }, function(){
            //$(this).parent().find("ul.subnav").slideUp('slow'); //When the mouse hovers out of the subnav, move it back up
            $(this).parent().find("ul.subnav").fadeOut('slow');
        });

        //Following events are applied to the trigger (Hover events for the trigger)
        }, function(){  //On Hover Out
        	$(this).find("span.sub").removeClass("subhover"); //On hover out, remove class "subhover"
    });

});
