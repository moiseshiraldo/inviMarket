// Check css transforms property support
var transforms = ["transform",
            "msTransform",
            "webkitTransform",
            "mozTransform",
            "oTransform"];
var transformProperty = getSupportedPropertyName(transforms);

function getSupportedPropertyName(properties) {
  for (var i = 0; i < properties.length; i++) {
    if (typeof document.body.style[properties[i]] != "undefined") {
      return properties[i];
    }
  }
  return null;
}

function startTimer(w) {
  w.timeoutID = window.setInterval(function(){GoToNextItem(w)}, 4000);
}

function resetTimer(w) {
  window.clearInterval(w.timeoutID);
  startTimer(w);
}

function pauseTimer(w) {
  window.clearInterval(w.timeoutID);
}

function changePosition(link) {
  link.classList.add("active");
  if (windowWidth < 720) {
    var position = link.getAttribute("data-mobPos");
  } else {
    var position = link.getAttribute("data-pos");
  }
  var wrapper = $("#" + link.getAttribute("data-section"));
  var translateValue = "translate3d(" + position + ", 0px, 0)";
  wrapper.css(transformProperty, translateValue);
}

function GoToNextItem(w) {
  removeActiveLinks(w);
  var activeLink = w.activeLink;
  if (activeLink < w.links.length - 1) {
    activeLink++;
    w.activeLink = activeLink;
  } else {
    w.activeLink = 0;
  }
  var newLink = w.links[w.activeLink];
  changePosition(newLink);
}

function removeActiveLinks(w) {
  for (var i = 0; i < w.links.length; i++) {
    w.links[i].classList.remove("active");
  }
}

function setClickedItem(e) {
    var clickedLink = e.target;
    var wrapper = document.getElementById(clickedLink.getAttribute("data-section"));
    removeActiveLinks(wrapper);
    resetTimer(wrapper);
    wrapper.activeLink = clickedLink.itemID;
    changePosition(clickedLink);
}

$(document).ready(function(){

  // Get wrappers and set links and timers for each one
  var wrappers = $(".wrapper");
  for (var i = 0; i < wrappers.length; i++) {
    wrappers[i].links = $("#" + wrappers[i].id + " + .slideButtons li");
    wrappers[i].links[0].classList.add("active");
    wrappers[i].timer = startTimer(wrappers[i]);
    for (var j = 0; j < wrappers[i].links.length; j++) {
      var link = wrappers[i].links[j];
      link.addEventListener('click', setClickedItem, false);
      link.itemID = j;
    }
  }

});

