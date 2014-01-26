/**
 * Created by oliver on 14.01.14.
 */
$.fn.searchTable = function (selector, options) {
    var searchTerm, regexp, rows, rowText;

    $.merge(options, {
        searchIn: []
    });

    if (typeof options.searchIn == "string") {
        var columns = $(selector).find('thead ' + options.searchIn);
        options.searchIn = columns.map(function () {
            return this.cellIndex + 1;
        });
        console.dir(columns);
    }

    // searchable cells
    $(options.searchIn).each(function () {
        $(selector).find('tbody > tr td:nth-child(' + this + ')').addClass('searchable-column');
    });

    $(this).on('keyup', function () {
        searchTerm = $(this).val();
        regexp = new RegExp(searchTerm, 'i');

        rows = $(selector).find('tbody > tr');

        rows.hide();
        rows.filter(function () {
            rowText = $(this).find('.searchable-column').text();
            return regexp.test(rowText);
        }).show();
    });
};
