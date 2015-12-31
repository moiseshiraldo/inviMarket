$(document).ready(function(){
    // Roto2 cursor
    var cursor_url = $( "#site article h1" ).data("cursor");
    $( "#site article" ).css("cursor", "url(" + cursor_url + "), auto");
});