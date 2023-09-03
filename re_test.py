import re

#The search() function returns a Match object:

txt = r'<span class="text">

    <a href="/" title="Home">Home</a>
    »


    <a href="/products/32283111">56" Green and Red Artificial Christmas Tree Storage Bag</a>

  </span>
  <!-- <div class="social clearfix">

    <div class="socitem facebookcont">
        <div class="fb-like" data-send="false" data-layout="button_count" data-width="80" data-show-faces="false"></div>
        <div id="fb-root"></div>
        <script>(function(d, s, id) {
        var js, fjs = d.getElementsByTagName(s)[0];
        if (d.getElementById(id)) return;
        js = d.createElement(s); js.id = id;
        js.src = "//connect.facebook.net/en_GB/all.js#xfbml=1&status=0";
        fjs.parentNode.insertBefore(js, fjs);
        }(document, 'script', 'facebook-jssdk'));</script>
    </div>

    <div class="socitem twittercont">
        <a href="https://twitter.com/share" class="twitter-share-button" data-count="none">Tweet</a>
        <script>!function(d,s,id){var js,fjs=d.getElementsByTagName(s)[0];if(!d.getElementById(id)){js=d.createElement(s);js.id=id;js.src="//platform.twitter.com/widgets.js";fjs.parentNode.insertBefore(js,fjs);}}(document,"script","twitter-wjs");</script>
    </div>

    <div class="socitem plusonecont">
        <g:plusone size="medium" annotation="none"></g:plusone>
        <script type="text/javascript" src="https://apis.google.com/js/plusone.js"></script>
    </div>


    <div class="socitem pinterestcont">
      <a href="http://pinterest.com/pin/create/button/?url=https://northlightseasonal.com/products/32283111&media=http://cdn.shopify.com/s/files/1/0447/2965/products/ly36bphb5dtjwnlsehqqe6nxljeuuzar.jpg?v=1600777248&description=56&quot; Green and Red Artificial Christmas Tree Storage Bag" class="pin-it-button" target="_blank" count-layout="none"><img border="0" src="//assets.pinterest.com/images/PinExt.png" title="Pin It" /></a>
      <script type="text/javascript" src="//assets.pinterest.com/js/pinit.js"></script>
    </div>



    <div class="socitem">
      <a id="FancyButton" data-count="false" href="http://www.thefancy.com/fancyit?ItemURL=https://northlightseasonal.com/products/32283111&Title=56&quot; Green and Red Artificial Christmas Tree Storage Bag&Category=Christmas Tree Accessories&ImageURL=http://cdn.shopify.com/s/files/1/0447/2965/products/ly36bphb5dtjwnlsehqqe6nxljeuuzar_grande.jpg?v=1600777248">Fancy</a>
      <script src="https://www.thefancy.com/fancyit.js" type="text/javascript"></script>
    </div>



</div> -->'
x = re.search("<div class=\"socitem\">(.*?|\n*?|\s*?)*<\/div>", txt)
print(x.sr())
