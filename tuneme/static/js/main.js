  var menuItems = new Array();

  function init() {
    // Grab the accordion items from the page
    var divs = document.getElementsByTagName( 'div' ); //Wild card?
    for ( var i = 0; i < divs.length; i++ ) {
      if ( divs[i].className == 'mainMenu' ||
          divs[i].className == 'mainMenu menuItem hide') {
          //Push div with class names mainMenu menuItems hide into an array
            menuItems.push( divs[i] );
      }
    }
    // Assign onclick events to the accordion item headings
    for ( var i = 0; i < menuItems.length; i++ ) {
      var span = getFirstChildWithTagName( menuItems[i], 'SPAN' );
      span.onclick = toggleItem;
    }
  }

  function toggleItem() {
    var itemClass = this.parentNode.className;

  // Hide all items
    for ( var i = 0; i < menuItems.length; i++ ) {
      menuItems[i].className = 'mainMenu menuItem hide';
    }

  // Show this item if it was previously hidden
    if ( itemClass == 'mainMenu menuItem hide' ) {
      this.parentNode.className = 'mainMenu menuItem';
    }

    if ( this.parentNode.id == "pages") {
      var logos = document.getElementsByClassName("logo");
      for (var i = 0; i < logos.length; i++) {
        if (logos[i].className == "logo") {
          logos[i].className = "logo hide";
        } else {
          logos[i].className = "logo";
        }
      }
    }

  }

  function getFirstChildWithTagName( element, tagName ) {
    for ( var i = 0; i < element.childNodes.length; i++ ) {
      if ( element.childNodes[i].nodeName == tagName ) return element.childNodes[i];
    }
  }
