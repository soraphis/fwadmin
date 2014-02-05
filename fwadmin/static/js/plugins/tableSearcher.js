/**
 * Created by oliver on 14.01.14.
 */
(function( $ ) {
  $.fn.searchTable = function (selector, options) {
    var searchTerm, regexp, rows, $row, rowText;
    var options = $.extend(true, {}, $.fn.searchTable.defaults, options);


    if (typeof options.searchIn == "string") {
      var columns = $(selector).find('thead ' + options.searchIn);
      options.searchIn = columns.map(function () {
        return this.cellIndex + 1;
      });
    }

    // searchable cells
    $(options.searchIn).each(function () {
      $(selector).find('tbody > tr td:nth-child(' + this + ')').addClass('searchTable-cell');
    });


    $(this).on('keyup', function () {
      searchTerm = $(this).val();
      regexp = new RegExp(searchTerm, 'i');

      rows = $(selector).find('tbody > tr');
      rows.each(function () {
        $row = $(this);
        rowText = $row.find('.searchTable-cell').text();
        regexp.test(rowText) ? $row.show() : $row.hide();
      });
    });
  };


  $.fn.searchTable.defaults = {
    searchIn: ".searchable"
  }


  $(document).ready(function() {
    var table;
    var filterInputs = $('input[data-searchTable]');

    filterInputs.each(function(){
      var $this = $(this);
      $this.searchTable('table[data-searchTable="' + $this.attr('data-searchTable') + '"]')
    })
  });
})(jQuery);