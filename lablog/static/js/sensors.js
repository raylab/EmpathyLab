'use strict'

const RecordButton = {
  create (isRecording) {
    const btn = document.createElement('button')
    this.set(btn, isRecording)
    return btn
  },
  set (btn, isRecording) {
    btn.className = 'js-record-button btn btn-sm ' +
      (isRecording ? 'btn-danger' : 'btn-secondary')
    btn.textContent = isRecording ? 'Stop' : 'Record'
    btn.setAttribute('data-active', isRecording)
  },
  getAll (container = document.body) {
    return container.querySelectorAll('.js-record-button')
  }
}

const Headset = {
  create (sensor, record, isRecording, showRecordButton) {
    const item = document.createElement('li')
    item.className = 'js-headset-item list-group-item d-flex justify-content-between align-items-center'
    item.setAttribute('data-channel', sensor)
    item.setAttribute('data-record', record)
    item.appendChild(document.createTextNode(sensor))
    if (showRecordButton) {
      const btn = RecordButton.create(isRecording)
      btn.addEventListener('click', function () {
        if (btn.getAttribute('data-active') === 'true') {
          WebAPI.stopRecording(sensor, item.getAttribute('data-record'))
        } else {
          item.dispatchEvent(new CustomEvent('startRecording'))
        }
      })
      item.appendChild(btn)
    }
    return item
  },

  set (item, record, isRecording) {
    item.setAttribute('data-record', record)
    const btns = RecordButton.getAll(item)
    for (let i = 0; i < btns.length; i++) {
      RecordButton.set(btns[i], isRecording)
    }
  },

  getAll (container = document.body) {
    return container.querySelectorAll('.js-headset-item')
  },

  getBySensorAll (container = document.body, sensor) {
    return container.querySelectorAll('.js-headset-item[data-channel="' + sensor + '"]')
  }
}

const HeadsetList = {
  addHeadset (list, sensor, record, isRecording) {
    const showRecordButton = list.hasAttribute('data-allow-recording')
    const item = Headset.create(sensor, record, isRecording, showRecordButton)
    item.addEventListener('startRecording', function (e) {
      WebAPI.startRecording(sensor, list.getAttribute('data-experiment'))
    })
    list.appendChild(item)
  },

  removeHeadset (list, sensor) {
    const items = Headset.getBySensorAll(list, sensor)
    for (let i = 0; i < items.length; i++) {
      items[i].parentNode.removeChild(items[i])
    }
  },

  setHeadset (list, sensor, record, isRecording) {
    const items = Headset.getBySensorAll(list, sensor)
    for (let i = 0; i < items.length; i++) {
      Headset.set(items[i], record, isRecording)
    }
  },

  getAll (container = document.body) {
    return container.querySelectorAll('.headsets-list')
  }
}

const RecordItem = {
  create (record) {
    const item = document.createElement('tr')
    item.setAttribute('data-record', record.id)
    this.set(item, record)
    return item
  },

  set (item, record) {
    item.innerHTML = '<td>' + record.id + '</td>' +
      '<td>' + record.StartTime + '</td>' +
      '<td>' + record.StopTime + '</td>' +
      '<td>' + record.ObservationMedia1 + '</td>' +
      '<td>' + record.ObservationMedia2 + '</td>' +
      '<td>' +
      '<a href="/lablog/record/' + record.id + '">View</a>, ' +
      '<a class="text-danger" href="/lablog/record/' + record.id + '/delete/">Delete</a>' +
      '</td>'
  },

  getByRecordID (container = document.body, id) {
    return container.querySelectorAll('tr[data-record="' + id + '"]')
  }
}

const RecordList = {
  addRecord (list, record) {
    list.appendChild(RecordItem.create(record))
  },
  setRecord (list, record) {
    const items = RecordItem.getByRecordID(list, record.id)
    for (let i = 0; i < items.length; i++) {
      RecordItem.set(items[i], record)
    }
  },
  getByExperimentID (container = document.body, id) {
    return container.querySelectorAll('.js-records-table[data-experiment="' + id + '"]')
  },
  getAll (container = document.body) {
    return container.querySelectorAll('.js-records-table')
  }
}

function onAddRecord (data) {
  const lists = RecordList.getByExperimentID(document.body, data.experiment)
  for (let i = 0; i < lists.length; i++) {
    RecordList.addRecord(lists[i], data.record)
  }
}

function onUpdateRecord (data) {
  const lists = RecordList.getAll()
  for (let i = 0; i < lists.length; i++) {
    RecordList.setRecord(lists[i], data.record)
  }
}

function onAddSensor (data) {
  const lists = HeadsetList.getAll()
  for (let i = 0; i < lists.length; i++) {
    HeadsetList.addHeadset(lists[i], data.sensor, data.record, data.is_recorded)
  }
}

function onRemoveSensor (data) {
  const lists = HeadsetList.getAll()
  for (let i = 0; i < lists.length; i++) {
    HeadsetList.removeHeadset(lists[i], data.sensor)
  }
}

function onUpdateSensor (data) {
  const lists = HeadsetList.getAll()
  for (let i = 0; i < lists.length; i++) {
    HeadsetList.setHeadset(lists[i], data.sensor, data.record, data.is_recorded)
  }
}

const WebAPI = {
  init (host) {
    this.socket = new WebSocket('ws://' + host + '/ws/api')
    this.socket.onmessage = function (e) {
      const data = JSON.parse(e.data)
      switch (data.command) {
        case 'add_sensor':
          onAddSensor(data)
          break
        case 'remove_sensor':
          onRemoveSensor(data)
          break
        case 'update_sensor':
          onUpdateSensor(data)
          break
        case 'add_record':
          onAddRecord(data)
          break
        case 'update_record':
          onUpdateRecord(data)
          break
      }
    }

    this.socket.onclose = function (e) {
      console.error('WebAPI socket closed unexpectedly')
    }
  },

  startRecording (sensor, experiment) {
    this.socket.send(JSON.stringify(
      {
        command: 'start_recording',
        channel: sensor,
        experiment: experiment
      }))
  },

  stopRecording (sensor, record) {
    this.socket.send(JSON.stringify(
      {
        command: 'stop_recording',
        channel: sensor,
        record: record
      }))
  }
}

WebAPI.init(window.location.host)
