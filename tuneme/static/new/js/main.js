"use strict";
(function() {
  var domReady = function(callback) {
      document.readyState === "interactive" || document.readyState === "complete" ? callback() : document.addEventListener("DOMContentLoaded", callback);
  };

  domReady(function() {

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
