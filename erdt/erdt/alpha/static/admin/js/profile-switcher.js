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