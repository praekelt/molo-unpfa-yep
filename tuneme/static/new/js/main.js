  /*var menuItems = new Array(),
      screenWidth = window.innerWidth;

  function init() {
    // Grab the accordion items from the page
    var divs = document.getElementsByTagName( 'div' );
    for ( var i = 0; i < divs.length; i++ ) {
      if ( divs[i].className == 'main-menu' ||
          divs[i].className == 'main-menu menu-item hide') {
            menuItems.push( divs[i] );
      }
    }

    // Assign onclick events to the accordion item headings
    for ( var i = 0; i < menuItems.length; i++ ) {
      var menu = getFirstChildWithTagName( menuItems[i], 'SPAN' );
      menu.onclick = toggleItem;
    }
  }



  function toggleItem() {
    var itemClass = this.parentNode.className;

  // Hide all items
    for ( var i = 0; i < menuItems.length; i++ ) {
      menuItems[i].className = 'main-menu menu-item hide';
    }

  // Show this item if it was previously hidden
    if ( itemClass == 'main-menu menu-item hide' ) {
      this.parentNode.className = 'main-menu menu-item';
    }

    if ( this.parentNode.id == "pages") {
      var logos = document.getElementsByClassName("logo");
      for (var i = 0; i < logos.length; i++) {
           if(screenWidth <= 320) {
            if (logos[i].className == "logo") {
                  logos[i].className = "logo hide";
                } else {
                  logos[i].className = "logo";
                }
           }
      }
    }
  }

  function getFirstChildWithTagName( element, tagName ) {
    for ( var i = 0; i < element.childNodes.length; i++ ) {
      if ( element.childNodes[i].nodeName == tagName ) return element.childNodes[i];
    }
  }*/


  //NEW JQUERY
(function() {
  var $parent_div = $('.image-article-col');
   $parent_div.each(function(i) {
      if ($(this).find("img").length > 0) {
           $(this).addClass('article-column')
      }
      else {
          $(this).removeClass('article-column')
      }
   });

})();

    var CutsTheMustard = 'querySelector' in document && 'localStorage' in window && 'addEventListener' in window,
        ScreenLargeEnough = ((window.innerWidth || document.documentElement.clientWidth || document.body.clientWidth) >= 200);
          if(CutsTheMustard === true)  {
              document.write('<link rel="stylesheet" type="text/x-scss" href="static/new/css/style.scss');
          } else {
             
          }

