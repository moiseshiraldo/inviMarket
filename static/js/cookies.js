$(document).ready(function(){

    // Get cookies and split them
    var cookies = document.cookie;
    var cookie = document.cookie.split(';');
    var viewed = false;

    // Search for the 'cookiesWarning' cookie
    for(var i=0; i<cookie.length; i++) {
        var c = cookie[i];
        while (c.charAt(0)==' ') c = c.substring(1);
        if (c.indexOf("cookiesWarning=viewed") == 0) viewed = true;
    }

    // Show the cookies warning if not viewed yet
    if (viewed == false) $( "#cookies").slideDown("slow");

    $( "#cookies .closeButton" ).click(function() {
        $( "#cookies" ).slideUp();
        document.cookie="cookiesWarning=viewed; path=/;";
    });

});