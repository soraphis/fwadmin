(function( $ ) {
  var getHostByName = function (name, singleCallback, multiCallback) {
    $.getJSON(app.urls.getHostByName(name), function(data) {
      typeof(singleCallback) == "function" &&
        data.length === 1 &&
        singleCallback(data[0]);

      typeof(multiCallback) == "function" &&
        data.length > 1 &&
        multiCallback(data);
    });
  };

  $(document).ready(function() {
    $((location.hash || '#simple') + '.collapse').collapse('show');

    // Resolve hostname
    $("#gethostbyname").click(function() {
      var name = $("#id_ip").val();
      var elem;

      getHostByName(name, function(data) {
        $("#id_ip").val(data);
      }, function(data) {
        $('#ip_list').empty();
        $(data).each(function(i, item) {
          elem = $("<option></option>")
                  .attr("value", item)
                  .text(item);
          $('#ip_list').append(elem);
        });
        $('#modalIPSelectionDialog').modal({});
      });
    });


    $("#id_name").change(function() {
      var $ip = $("#id_ip");
      var name = $("#id_name").val();
      if( $ip.val() === "") {
        getHostByName(name, function(data) {
          $ip.val(data);
        });
      }
    });


    // Setup QuickSetup buttons
    $("button[data-quick-setting-protocol]").click(function() {
      var $this = $(this);
      $("#id_ip_protocol").val($this.data("quick-setting-protocol"));
      $("#id_port_range").val($this.data("quick-setting-port"));
      $("#id_name").val($this.data("quick-setting-name"));
      $("#id_from_net").val($this.data("quick-setting-from"));
    })


    // keep id_stock_port and id_port in sync
    // TODO: replace parsing with data-attributes
    $("#id_stock_port").change(function() {
      var selected_str = $("#id_stock_port option:selected").text();
      var regexp = selected_str.match(/(\w+)(.*)\((.*)\)/);
      var ip_protocol = regexp[1];
      var name = regexp[2];
      var port = regexp[3];
      $("#id_ip_protocol").val(ip_protocol);
      $("#id_port_range").val(port);
      $("#id_name").val(name);
      $("#id_from_net").val("any");
    });


    // reset id_stock_port when id_port changes
    $("#id_port_range").change(function() {
       $("#id_stock_port").val("");
    });
  });
})(jQuery);