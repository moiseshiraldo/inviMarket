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
  // Scroll filter form
  if (y_scroll > 12*0.9*16) { // 15em * 0.9 (font-size) * 16 px/em
    $(".filter form").css("top", "5em");
    }
  else {
    position = 18*0.9*16 - y_scroll;
    $(".filter form").css("top", position + "px");
  }
});

// Roto2 cursor
if ( $( "#site h1" ).text().indexOf("ForoCoches") >= 0 ) {
  $( "#site" ).css("cursor", "url('/static/images/roto2.png'), auto");
}

});