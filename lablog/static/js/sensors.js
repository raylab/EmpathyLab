document.addEventListener("DOMContentLoaded", function() {

  function recordClicked() {
    var is_recorded = this.getAttribute("data-active");
    var sensor = this.getAttribute("data-channel");
    if (is_recorded == 'true') {
      var record = this.getAttribute("data-record");
      webapi.send(JSON.stringify(
        {
          command: "stop_recording",
          channel: sensor,
          record: record,
        }));
    } else {
      var experiment = this.getAttribute("data-experiment");
      webapi.send(JSON.stringify(
        {
          command: "start_recording",
          channel: sensor,
          experiment: experiment,
        }));
    }
  }

  var webapi = new WebSocket('ws://' + window.location.host + '/ws/api');

  webapi.onmessage = function(e) {
    var data = JSON.parse(e.data);
    var command = data['command'];
    if(command == 'add_sensor') {
      var sensor = data['sensor']
      var is_recorded = data['is_recorded']
      var record = data['record']
      var headsets_lists = document.querySelectorAll(".headsets-list");
      for (var i = 0; i < headsets_lists.length; i++) {
        var sensor_item = document.createElement("li");
        sensor_item.className = "list-group-item d-flex justify-content-between align-items-center";
        sensor_item.setAttribute("data-channel", sensor);
        sensor_item.appendChild(document.createTextNode(sensor));
        var experiment = headsets_lists[i].getAttribute("data-experiment");
        if (experiment) {
          var record_button = document.createElement("button");
          record_button.className = "btn btn-sm " + (is_recorded  ? "btn-danger": "btn-secondary");
          record_button.setAttribute("data-channel", sensor);
          record_button.setAttribute("data-record", record);
          record_button.setAttribute("data-active", is_recorded);
          record_button.setAttribute("data-experiment", experiment);
          record_button.textContent = is_recorded ? "Stop" : "Record";
          record_button.addEventListener('click', recordClicked, false);
          sensor_item.appendChild(record_button);
        }
        headsets_lists[i].appendChild(sensor_item);
      }
    } 
    else if(command == 'remove_sensor') {
      var sensor = data['sensor'];
      var sensor_items = document.querySelectorAll("li[data-channel=\""+ sensor +"\"]");
      for (var i = 0; i < sensor_items.length; i++) {
        sensor_items[i].parentNode.removeChild(sensor_items[i]);
      }
    } else {
      var sensor = data['sensor']
      var is_recorded = data['is_recorded']
      var record = data['record']
      var record_buttons = document.querySelectorAll("button[data-channel=\""+ sensor +"\"]");
      for (var i = 0; i < record_buttons.length; i++) {
        record_buttons[i].className = "btn btn-sm " + (is_recorded ? "btn-danger": "btn-secondary");
        record_buttons[i].setAttribute("data-active", is_recorded);
        record_buttons[i].setAttribute("data-record", record);
        record_buttons[i].textContent = is_recorded  ? "Stop" : "Record";
      }
    }
  };

  webapi.onclose = function(e) {
    console.error('WebAPI socket closed unexpectedly');
  };
});
