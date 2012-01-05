/**
 * simpletooltip.js
 * Simple Tooltip
 * Copyright (c) 2009 SGT Dev.
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * View the GNU General Public License <http://www.gnu.org/licenses/>.
 *
 * @author Sergio Gabriel Teves (info at sgtdev.com.ar)
 * @date 05/02/2009
 * @version 1.0.1
 * 
 * @requires jquery.js (tested with 1.3.2)
 * 
*/

( function( $ ) {
   $.fn.tooltip = function( o, callback ) {
       o = $.extend( { 
           className: null,
       }, o || {});
    
       var topOffset = -5;
       var leftOffset = -25;
       var maxWidth = 502; // px
       
       $(this).hover(
		      function (ev) {
		          var text = $(this).attr('alt')
		          var div = '<div class="'+o.className+'" style="position: absolute; display: none;">';
		          div += '<div class="tip-tl"><div class="tip-tr"><div class="tip-tc"></div></div></div>';
		          div += '<div class="tip-bwrap"><div class="tip-ml"><div class="tip-mr"><div class="tip-mc"><div class="tip-body">';
		          div += text;
		          div += '</div></div></div></div></div><div class="tip-bl"><div class="tip-br"><div class="tip-bc"></div></div></div></div>';
		    	  $(this).append(div);
				  var tooltip = $(this).find("div:." + o.className);
				  var p = $(this).position();
				  var w = tooltip.width();
				  if (w > maxWidth) w = maxWidth;
				  tooltip.css("top",(p.top+topOffset)+"px");
				  tooltip.css("left",($(this).width()+p.left+leftOffset)+"px");
				  tooltip.show();
				  tooltip.css("width",w);
		      }, 
		      function () {
		    	  $(this).find("div:." + o.className).remove();
		      }
       );

   }
})( jQuery );