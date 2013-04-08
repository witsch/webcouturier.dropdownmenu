/* The following line defines global variables defined elsewhere. */
/*globals $, jQuery*/

jQuery(function ($) {
    $('#portal-globalnav .noClick').click(function (e) {
        e.preventDefault();
    });
});

jQuery('ul.nav li.dropdown').hover(function() {
    jQuery(this).closest('.dropdown-menu').stop(true, true).show();
    jQuery(this).addClass('open');
}, function() {
    jQuery(this).closest('.dropdown-menu').stop(true, true).hide();
    jQuery(this).removeClass('open');
});
