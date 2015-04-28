var windowWidth = window.innerWidth || $(window).width();

$( window ).resize(function() {
  windowWidth = window.innerWidth || $(window).width();
});

$(document).ready(function(){

// Fix nav menu when scrolling down
$(window).scroll(function(){
  var y_scroll = $(this).scrollTop();
  if (windowWidth > 479) {
    if (y_scroll > 80) {
      $("header").css({position: "fixed", top: "-79px"});
    } else {
      $("header").css({position: "absolute", top: "0em"});
    }
  }
  else {
    if (y_scroll > 70) {
      $("header").css({position: "fixed", top: "-71px"});
    } else {
      $("header").css({position: "absolute", top: "0em"});
    }
  }
  if (y_scroll > 150) {
    $(".filter form").css("top", "5em");
    }
  else {
    position = 259 - y_scroll;
    $(".filter form").css("top", position + "px");
  }
});

  if ( $( "#site h1" ).text().indexOf("Forocoches") >= 0 ) {
      $( "#site" ).css("cursor", "url('/static/images/roto2.png'), auto");
  }

});