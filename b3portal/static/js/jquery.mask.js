/**
 * Copyright (c) 2010, Nathan Bubna
 * Dual licensed under the MIT and GPL licenses:
 *   http://www.opensource.org/licenses/mit-license.php
 *   http://www.gnu.org/licenses/gpl.html
 *
 * This plugin makes it trivial to mask an element or the
 * whole page. Just use:
 * 
 *   $.mask();
 *
 * to toggle a page-wide message on and off, or you can call:
 *
 *   $('#foo').mask()
 *
 * to do the same, but restrict the mask to any specific element(s).
 *
 * If you want to ensure that a call doesn't errantly toggle on when
 * you meant to toggle off (or vice versa), then put a boolean value
 * as your first argument.  true is on, false is off.
 *
 *   $.mask(false); // will only ever toggle off
 *   $.mask(true, {maskCss:{background:'#666'}});  // will only ever toggle on
 *
 * You can change any of the default options by altering the $.mask
 * properties (or sub-properties), like this:
 *
 *  $.mask.maskClass = 'mask';
 *  $.mask.maskCss.border = '1px solid #F00';
 *
 * All options can also be overridden per-call by passing in
 * an options object with the overriding properties, like so:
 *
 *  $.mask({ block:false });
 *  $('#foo').mask(true, { resize:false });
 *
 * And if that isn't enough, this plugin supports the metadata plugin as a
 * way to specify options directly in your markup.
 *
 * Be sure to check out the provided demo for an easy overview of the most
 * commonly used options!! Of course, everything in this plugin is easy to
 * configure and/or override with those same techniques.
 *
 * To style the mask or masked element in your CSS files, it's good to know
 * that by default, the mask itself is given the 'mask' class, and the
 * element (or page body) being masked is given the 'masked' class.
 *
 * Finally, this plugin will trigger 'maskStart'
 * and 'maskStop' events when loading is turned on and off, respectively.
 * The options will, of course, be available as a second argument to functions
 * that are bound to these events.  See the demo source for an example. In
 * future versions, this plugin itself may use those events, but for now they
 * are merely notifications.
 *
 * Contributions, bug reports and general feedback on this is welcome.
 *
 * @version 1.0
 * @requires $.measure
 * @name mask
 * @author Nathan Bubna
 */
;(function($) {
    // enforce requirement(s)
    if (!$.measure) throw '$.mask plugin requires $.measure plugin to be present';

    // the main interface...
    $.mask = function(show, opts) {
        return $('body').mask(show, opts);
    };
    var M = $.fn.mask = function(show, opts) {
        opts = M.toOpts(show, opts);
        M.plugin.call(this, $.mask, opts, M.toggle);
        return this;
    };

    // all that's configurable...
    $.extend(true, $.mask, $.measure, test = {
        version: "1.0",
        block: true,
        resize: true,
        maskClass: 'mask',
        maskedClass: 'masked',
        maskCss: { position:'absolute', opacity:.15, background:'#333',
                   zIndex:101, display:'block', cursor:'wait' },
        maskHtml: '<div></div>',
        pageOptions: { maskCss: $.measure.fixedCss },
        resizeEvents: 'resize',
        blockEvents: 'mousedown mouseup keydown keypress focusin'
    });

    // all that's extensible...
    $.extend($.fn.mask, $.fn.measure, {
        toggle: function(o) {
            var old = this.data('mask');
            if (old) {
                if (o.show !== true) M.off.call(this, old, o);
            } else {
                if (o.show !== false) M.on.call(this, o);
            }
        },
        on: function(o) {
            var self = this;
            o.mask = M.create.call(this, o);
            this.data('mask', o);
            if (o.resize) {
                o.resizer = function(e) { return M.resizeHandler.call(self, e, o); };
                $(window).bind(o.resizeEvents, o.resizer);
            }
            if (o.block) {
                o.blocker = function(e) { return M.blockHandler.call(self, e, o); };
                $(document).bind(o.blockEvents, o.blocker);
            }
            this.trigger('maskStart', [o]);
        },
        create: function(o) {
            var box = M.measure.call(this.addClass(o.maskedClass), o);
            return $(o.maskHtml).addClass(o.maskClass)
                .css(box).css(o.maskCss).appendTo(this);
        },
        resizeHandler: function(e, o) {
            this.box = null;
            o.mask.hide();
            M.measure.call(this, m);
            o.mask.show().css(this.box);
        },
        blockHandler: function(e, o) {
            if (e.type == 'focusin') $(e.target).blur();
            var $els = $(e.target).parents().andSelf();
            return !o.page && $els.filter('.'+o.maskedClass).length == 0;
        },
        off: function(o, newO) {
            if (o.resize) $(window).unbind(o.resizeEvents, o.resizer);
            if (o.block) $(document).unbind(o.blockEvents, o.blocker);
            o.mask.remove();
            this.data('mask', null).removeClass(o.maskedClass)
                .trigger('maskStop', [o]);
        },
        toOpts: function(show, o) {
            if (o === undefined) {
                o = (typeof show == "boolean") ? { show: show } : show;
            } else {
                o.show = show;
            }
            return o;
        }
    });

})(jQuery);
