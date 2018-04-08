$( document ).ready(function() {
  var webapi = new WebSocket('ws://' + window.location.host + '/ws/api');

  webapi.onmessage = function(e) {
    var data = JSON.parse(e.data);
    var command = data['command'];
    if(command == 'add_sensor') {
      var sensor = data['sensor']
      var id = sensor.replace(/\./g, '_').replace(/\!/g, '_')
      $(".headsets-list").append("<li class=\"list-group-item\" id=\"" + id + "\">" +sensor+"</li>");
    } 
    else if(command == 'remove_sensor') {
      var sensor = data['sensor']
      var id = sensor.replace(/\./g, '_').replace(/\!/g, '_')
      $('#'+id).remove();
    }
  };

  webapi.onclose = function(e) {
    console.error('WebAPI socket closed unexpectedly');
  };
});
