$(document).ready(function(){

    // Show/hide notifications
    $( "#notifications" ).click(function(event) {
        $( "#notifications .messages-list" ).slideToggle();
        $( "#notifications .arrow").slideToggle();
        event.stopPropagation();
    });

    // Show/hide mobile menu
    if (windowWidth < 720) {
        $( "#menu-button").click(function(event) {
            $( ".menu-item" ).slideToggle();
            event.stopPropagation();
        });
    }

    // Hide notifications and mobile menu when clicking outside
    $(document).click(function() {
        $( "#notifications .messages-list" ).slideUp();
        $( "#notifications .arrow").slideUp();
        if ( (windowWidth < 720) && $( ".menu-item" ).css("display") !=
              "none" ) {
            $( ".menu-item" ).slideUp();
        }
    });

    // Stop click propagation
    $(".messages-list").click(function(event) {
        event.stopPropagation();
    });

    $(".mobile-menu").click(function(event) {
        event.stopPropagation();
    });

    // Show/hide sites lists (<920px)
    if (windowWidth < 920) {
        $( ".showButton" ).click(function() {
            $( this ).parents(".sitesList").children( "ul" ).slideToggle();
            var label = $( this ).children( "span");
            if ( label.text() == "Show" ) {
                label.text("Hide")
            } else {
                label.text("Show")
            }
        });
    }

    // Slide aside filter forms (<480px)
    if (windowWidth < 480) {
        $( ".slideButton" ).click(function() {
            if ( $( ".slideButton" ).text() == ">>" ) {
                $( ".filter form" ).css("left", "-1em");
                $( ".slideButton" ).text("<<");
            } else {
                $( ".filter form" ).css("left", "-12em");
                $( ".slideButton" ).text(">>");
            }
        });
    }

    // Show/hide options list in filter forms
    $( ".showOptions" ).click(function() {
        if ( $( this ).text() == "+" ) {
            $( this ).next().children("li").slideDown();
            $( this ).text("-");
        } else {
            $( this ).next().children("li").slideUp();
            $( this ).text("+");
        }
    });

    // Show/hide site description
    $( ".descriptionButton").click(function() {
        var arrow = $( this ).children("img");
        var des = $( this ).parent().children( ".description" );
        if ( arrow.hasClass( "flipped" ) ) {
            des.slideUp();
            arrow.removeClass("flipped");
        }
        else {
            des.load($( this ).data("url") + " article p");
            des.slideDown();
            arrow.addClass("flipped");
        }
    });

    // Slide up current page and load link
    $( ".downButton" ).click(function() {
        $( this ).parent().slideUp(1000);
        $( ".filter" ).hide(2000);
        var header = $( this ).children("h2");
        switch ( header.data("next") ) {
            case 'register':
                // Load register page
                $( "#register" ).load(header.data("url") +
                                      " #register h1, .form, .help");
                break;
            case 'sites':
                // Load sits page
                $( "#sites" ).load(header.data("url") +
                                   " #sites .content, #sites aside");
                break;
            case 'market':
                // Load javascript for sliders and market page
                $.getScript(header.data("sliders"));
                $( "#market" ).load(header.data("url") +
                                    " .container, .smallContainer", function(){
                    // Initialize sliders
                    var wrappers = $(".wrapper");
                    for (var i = 0; i < wrappers.length; i++) {
                        wrappers[i].links = $("#" + wrappers[i].id +
                                              " + .slideButtons li");
                        wrappers[i].links[0].classList.add("active");
                        wrappers[i].timer = startTimer(wrappers[i]);
                        for (var j = 0; j < wrappers[i].links.length; j++) {
                            var link = wrappers[i].links[j];
                            link.addEventListener('click',
                                                  setClickedItem,
                                                  false);
                            link.itemID = j;
                        }
                    }
                });
        }
        $('html, body').animate({scrollTop:0}, 1000);
    });

});
