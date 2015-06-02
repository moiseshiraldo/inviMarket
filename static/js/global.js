var windowWidth = window.innerWidth || $(window).width();
var windowHeight = window.innerHeight || $(window).height();

$( window ).resize(function() {
    windowWidth = window.innerWidth || $(window).width();
    windowHeight = window.innerHeight || $(window).height();
});

$(document).ready(function(){

    // Fix nav menu when scrolling down
    $(window).scroll(function(){
        var y_scroll = $(this).scrollTop();
        if (windowWidth >= 480) {
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
        if (windowHeight > 480) {
            if (y_scroll > 12*0.9*16) { // 15em * 0.9 (font-size) * 16 px/em
                $(".filter form").css("top", "5em");
            } else {
                position = 18*0.9*16 - y_scroll;
                $(".filter form").css("top", position + "px");
            }
        }
    });

});