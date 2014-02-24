(function( $ ) {
  $(document).ready(function() {
    $("#show-js").removeClass("show-js"); // Show element if js is available
    $('.nav-tabs a[href='+location.hash+']').tab('show'); // Show tab on page load


    $('#button_select_ip').click(function() {
      var ip = $('#ip_list').find(":selected").text();
      $('#id_ip').val(ip);
      $('#modalIPSelectionDialog').modal('hide');
    });


    $('#rulesDialog button.btn-primary').click(function() {
        $('#rulesDialog').modal('hide');
        $('#id_check').prop('checked', true);
    });
  })
})( jQuery );