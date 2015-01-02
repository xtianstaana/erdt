/**********************************************
ERDT Profile Swicther script
Author: Christian Sta.Ana
Date: Sun Aug 3 2014
Description: Shows/Hides profile switcher
**********************************************/

jQuery(document).ready(function($) {

    $("#user-tools .active-profile").click(function(e) {
        e.preventDefault();

        $("#profile-switcher-container").fadeIn(300);
    });

    $("#profile-switcher .cancel-btn").click(function(e) {
        e.preventDefault();

        $("#profile-switcher-container").fadeOut(300);
    });



});

function showPopupSelected(triggeringLink) {
    var name = triggeringLink.id.replace(/^add_/, '');
    name = id_to_windowname(name);
    var href = triggeringLink.href;
    if (href.indexOf('?') == -1) {
        href += '?_popup=1';
    } else {
        href  += '&_popup=1';
    }
    var win = window.open(href, name, 'height=500,width=1100,resizable=yes,scrollbars=yes');
    win.focus();
    return false;
}