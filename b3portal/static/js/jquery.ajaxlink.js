/*
Copyright (c) 2012 Sergio Gabriel Teves
All rights reserved.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/

(function($){

    $.fn.ajaxlink = function(options){

        var opts = $.extend({}, $.fn.ajaxlink.defaults, options);
        var success = opts.success || function() { };
        var selector = $(this).selector;
        return $(this).each(function(){
            jQuery(document).on('click', selector, function() {
                var url  = $(this).attr("href");
                var div = $(this).prop("success");
                
                if (div == undefined) {
                	div = success;
                }
                
                if (!jQuery.isFunction(div)) {
                	func = function(data, status, jq) {
                		console.log(data);
                		var nid = "#"+div;
                		console.log(nid)
                		var html = $(nid, data).html();
                		console.log(html);
                		$(nid).html(html);
                	}
                } else {
                	func = div;
                }
                
                opts["url"] = url;
                opts["success"] = func;
                opts["dataType"] = "html";
                if (opts["oncomplete"]) { opts["oncomplete"](); }
                $.ajax( opts );
                return false;
            })
        });
    };
    $.fn.ajaxlink.defaults = {};
    
})(jQuery);
