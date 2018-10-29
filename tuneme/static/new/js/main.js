"use strict";
(function() {
  var domReady = function(callback) {
      document.readyState === "interactive" || document.readyState === "complete" ? callback() : document.addEventListener("DOMContentLoaded", callback);
  };

  domReady(function() {
    var selectRadius = document.getElementById('select_radius');
    if(selectRadius){
        console.log(selectRadius[selectRadius.selectedIndex].value);
        // get selected option in sel (reference obtained above)
        var optFunc = getSelectedOption(selectRadius);
        selectRadius.addEventListener('click', function() {
          console.log( optFunc.value," - ", optFunc.text);
        });
    }

    function getSelectedOption(sel) {
      var opt;
      for ( var i = 0, len = sel.options.length; i < len; i++ ) {
          opt = sel.options[i];
            console.log("List options ",opt);
          if ( opt.selected === true ) {
            //First assign selected
              break;
          }
      }
      return opt;
    }

    // Display select all field set
    // toggle selection on click
    var selectAllKaywords = $('#all_keywords');
    var parent = $(selectAllKaywords).parent().parent();
    $(parent).css('display', 'block');

    $(selectAllKaywords).on('click', function () {
        $(parent).siblings('.fieldset-group').each(function () {
            $(this).find('input').prop('checked', $(selectAllKaywords).is(':checked'));
        });
    });
  });
})();
