$(document).ready(function(){

  // Google
  (function() {
    var po = document.createElement('script'); po.type = 'text/javascript'; po.async = true;
    po.src = 'https://apis.google.com/js/plusone.js';
    var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(po, s);
  })();

  // Facebook
  (function(d, s, id) {
    var js, fjs = d.getElementsByTagName(s)[0];
    if (d.getElementById(id)) return;
    js = d.createElement(s); js.id = id;
    js.src = "//connect.facebook.net/en_GB/sdk.js#xfbml=1&version=v2.0";
    fjs.parentNode.insertBefore(js, fjs);
  }(document, 'script', 'facebook-jssdk'));

  // Twitter
  window.twttr=(function(d,s,id){
    var js,fjs=d.getElementsByTagName(s)[0],t=window.twttr||{};
    if(d.getElementById(id))return;
    js=d.createElement(s);
    js.id=id;js.src="https://platform.twitter.com/widgets.js";
    fjs.parentNode.insertBefore(js,fjs);t._e=[];
    t.ready=function(f){ t._e.push(f); };
    return t;
  }(document,"script","twitter-wjs"));

  if(typeof wabtn4fg==="undefined") {
    wabtn4fg=1;
    h=document.head||document.getElementsByTagName("head")[0],s=document.createElement("script");
    s.type="text/javascript";
    s.src="/static/js/whatsapp-button.js";
    h.appendChild(s);
  }

});