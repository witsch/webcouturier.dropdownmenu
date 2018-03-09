/* The following line defines global variables defined elsewhere. */
/* globals $, jQuery, window */

/* do not include jquery multiple times */
if (window.jQuery){
  define('jquery', [], function(){
    return window.jQuery;
  });
}

require([
  'jquery'
], function($){
  'use strict';

    jQuery(function ($) {
        $('#portal-globalnav .noClick').click(function (e) {
            e.preventDefault();
        });

        // $('ul.nav li.dropdown').hover(function() {
        //     $(this).closest('.dropdown-menu').stop(true, true).show();
        //     $(this).addClass('open');
        // }, function() {
        //     $(this).closest('.dropdown-menu').stop(true, true).hide();
        //     $(this).removeClass('open');
        // });
        var open_class = 'menu-open';
        $('ul.nav li.dropdown .opener').click(function(e) {
            e.preventDefault();
            $(this).toggleClass(open_class);
            $(this).parent().next('.dropdown-menu').toggleClass(open_class);
            // an accordion like behavior.
            var sibls = $(this).parents('li').siblings();
            sibls.each(function() {
                var still_open = $(this).find('.' + open_class);
                still_open.each(function() {
                    $(this).toggleClass(open_class);
                });
            });
        });
    });

});
