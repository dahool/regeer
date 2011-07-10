$(document).ready( function() {
	$("ul.dropdown li").dropdown();
	if (jQuery.browser.msie) {
		var zIndexNumber = 1000;
		$('div').each( function() {
			$(this).css('zIndex', zIndexNumber);
			zIndexNumber -= 10;
		});
	}
});

$.fn.dropdown = function() {
	$(this).hover( function() {
		$(this).addClass("hover");
		$('> .dir', this).addClass("open");
		$('ul:first', this).css('visibility', 'visible');
	}, function() {
		$(this).removeClass("hover");
		$('.open', this).removeClass("open");
		$('ul:first', this).css('visibility', 'hidden');
	});
}
