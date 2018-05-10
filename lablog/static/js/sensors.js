const RecordButton = {
  create(isRecording) {
    const btn = document.createElement('button');
    this.set(btn, isRecording);
    return btn;
  },
  set(btn, isRecording) {
    const dom = btn;
    dom.className = `js-record-button btn btn-sm ${
      isRecording ? 'btn-danger' : 'btn-secondary'}`;
    dom.textContent = isRecording ? 'Stop' : 'Record';
    dom.setAttribute('data-active', isRecording);
  },
  getAll(container = document.body) {
    return container.querySelectorAll('.js-record-button');
  },
};

function map(n, start1, stop1, start2, stop2) {
  return (n - start1) / (stop1 - start1) * (stop2 - start2) + start2;
}

const Chart = {
  queues: {},
  header: ['COUNTER', 'INTERPOLATED', 'RAW_CQ', 'AF3', 'F7', 'F3', 'FC5', 'T7', 'P7', 'O1', 'O2', 'P8', 'T8', 'FC6', 'F4', 'F8', 'AF4', 'GYROX', 'GYROY', 'TIMESTAMP', 'MARKER_HARDWARE', 'ES_TIMESTAMP', 'FUNC_ID', 'FUNC_VALUE', 'MARKER', 'SYNC_SIGNAL'],
  emoNames: ['Stress', 'Engagement', 'Relaxation', 'Exitement', 'Interest'],
  emoParams: ['Raw', 'Min', 'Max', 'Scaled'],
  emostates: {},
  create(sensor) {
    const chart = document.createElement('canvas');
    chart.height = 540;
    chart.width = 600;
    chart.className = 'js-sensors-chart';
    this.queues[sensor] = [];
    this.emostates[sensor] = {
      Stress: {
        Raw: 0, Min: 0, Max: 0, Scaled: 0,
      },
      Engagement: {
        Raw: 0, Min: 0, Max: 0, Scaled: 0,
      },
      Relaxation: {
        Raw: 0, Min: 0, Max: 0, Scaled: 0,
      },
      Exitement: {
        Raw: 0, Min: 0, Max: 0, Scaled: 0,
      },
      Interest: {
        Raw: 0, Min: 0, Max: 0, Scaled: 0,
      },
    };
    return chart;
  },
  drawDroppedPackets(chart, frames) {
    const ctx = chart.getContext('2d');
    const cnt = frames.length;
    ctx.strokeStyle = 'rgb(255,0,0)';
    if (cnt > 1) {
      for (let i = cnt - 1; i >= 1; i -= 1) {
        const tNew = frames[i].COUNTER;
        const tOld = frames[i - 1].COUNTER;

        if (i > 40 && tOld != ((tNew - 1) % 256)) {
          ctx.beginPath();
          ctx.moveTo(i, 20);
          ctx.lineTo(i, chart.height - 60);
          ctx.stroke();
        }
      }
    }
  },
  drawElectrodeData(chart, frames) {
    const ctx = chart.getContext('2d');
    const cnt = frames.length;
    if (cnt > 0) {
      for (let chan = 3; chan < 16; chan += 1) {
        const y = map(chan, 3, 15, 70, chart.height - 70);
        let x = chart.width - 1;
        ctx.fillStyle = 'rgb(255,255,255)';
        ctx.fillText(this.header[chan], 5, y);
        ctx.beginPath();
        ctx.strokeStyle = 'rgb(255,255,255)';
        const initial = frames[cnt - 1][this.header[chan]];
        ctx.moveTo(x, y + (initial - 4200) * 0.5);
        for (let i = cnt - 1; i >= 0; i -= 1) {
          const frame = frames[i];
          const value = frame[this.header[chan]];
          ctx.lineTo(x--, y + (value - 4200) * 0.5);
          if (x === 40) { break; }
        }
        ctx.stroke();
      }
    }
  },
  drawTimeGrid(chart, frames) {
    const ctx = chart.getContext('2d');
    const cnt = frames.length;
    ctx.strokeStyle = 'rgb(120,120,120)';
    ctx.fillStyle = 'rgb(120,120,120)';
    if (cnt > 1) {
      for (let i = cnt - 1; i >= 1; i -= 1) {
        const tNew = frames[i].TIMESTAMP;
        const tOld = frames[i - 1].TIMESTAMP;

        if (i > 40 && Math.floor(tNew) !== Math.floor(tOld)) {
          ctx.beginPath();
          ctx.moveTo(i, 20);
          ctx.lineTo(i, chart.height - 60);
          ctx.stroke();
          ctx.fillText(Math.floor(tNew), i - 8, 16);
        }
      }
    }
  },
  drawEmostate(chart, emostate) {
    const ctx = chart.getContext('2d');
    ctx.strokeStyle = 'white';
    ctx.fillStyle = 'white';
    const emoNamesLength = this.emoNames.length;
    const y = chart.height - 46;
    for (let i = 0; i < emoNamesLength; i++) {
      const x = map(i, 0, emoNamesLength, 5, chart.width - 5);
      const emo = emostate[this.emoNames[i]];
      ctx.fillText(`${this.emoNames[i]} Raw:${emo.Raw}`, x, y);
      ctx.fillText(`${this.emoNames[i]} Min:${emo.Min}`, x, y + 14);
      ctx.fillText(`${this.emoNames[i]} Max:${emo.Max}`, x, y + 28);
      ctx.fillText(`${this.emoNames[i]} Scaled:${emo.Scaled}`, x, y + 42);
    }
  },
  draw(chart, frames, emostate = null) {
    const ctx = chart.getContext('2d');
    if (chart.width !== chart.clientWidth || chart.height !== chart.clientHeight) {
      chart.width = chart.clientWidth;
      chart.height = chart.clientHeight;
    }
    ctx.fillStyle = 'black';
    ctx.fillRect(0, 0, chart.width, chart.height);
    this.drawTimeGrid(chart, frames);
    this.drawElectrodeData(chart, frames);
    this.drawDroppedPackets(chart, frames);
    this.drawEmostate(chart, emostate);
  },
  getAll(container = document.body) {
    return container.querySelectorAll('.js-sensors-chart');
  },
};

const Headset = {
  create(sensor, record, isRecording, showRecordButton) {
    const item = document.createElement('li');
    item.className = 'js-headset-item list-group-item d-flex flex-column';
    item.setAttribute('data-channel', sensor);
    item.setAttribute('data-record', record);
    const header = document.createElement('div');
    header.className = 'd-flex justify-content-between align-items-center';
    header.appendChild(document.createTextNode(sensor));
    if (showRecordButton) {
      const btn = RecordButton.create(isRecording);
      btn.addEventListener('click', () => {
        if (btn.getAttribute('data-active') === 'true') {
          WebAPI.stopRecording(sensor, item.getAttribute('data-record'));
        } else {
          item.dispatchEvent(new CustomEvent('startRecording'));
        }
      });
      header.appendChild(btn);
    }
    item.appendChild(header);
    item.appendChild(Chart.create(sensor));
    return item;
  },

  set(item, record, isRecording) {
    item.setAttribute('data-record', record);
    const btns = RecordButton.getAll(item);
    for (let i = 0; i < btns.length; i += 1) {
      RecordButton.set(btns[i], isRecording);
    }
  },

  drawData(item, data) {
    const charts = Chart.getAll(item);
    for (let i = 0; i < charts.length; i += 1) {
      const frames = Chart.queues[item.getAttribute('data-channel')];
      let emostate = Chart.emostates[item.getAttribute('data-channel')];
      Array.prototype.push.apply(frames, data.frames);
      if (frames.length > charts[i].width) {
        frames.splice(0, frames.length - charts[i].width);
      }
      if ('Emostate' in data) {
        emostate = data.Emostate;
        Chart.emostates[item.getAttribute('data-channel')] = emostate;
      }
      item.firstChild.firstChild.nodeValue = data.RecordNumber;
      window.requestAnimationFrame(() => {
        Chart.draw(charts[i], frames, emostate);
      });
    }
  },

  getAll(container = document.body) {
    return container.querySelectorAll('.js-headset-item');
  },

  getBySensorAll(container = document.body, sensor) {
    return container.querySelectorAll(`.js-headset-item[data-channel="${sensor}"]`);
  },
};

const HeadsetList = {
  addHeadset(list, sensor, record, isRecording) {
    const showRecordButton = list.hasAttribute('data-allow-recording');
    const item = Headset.create(sensor, record, isRecording, showRecordButton);
    item.addEventListener('startRecording', () => {
      WebAPI.startRecording(sensor, list.getAttribute('data-experiment'));
    });
    list.appendChild(item);
  },

  removeHeadset(list, sensor) {
    const items = Headset.getBySensorAll(list, sensor);
    for (let i = 0; i < items.length; i += 1) {
      items[i].parentNode.removeChild(items[i]);
    }
  },

  setHeadset(list, sensor, record, isRecording) {
    const items = Headset.getBySensorAll(list, sensor);
    for (let i = 0; i < items.length; i += 1) {
      Headset.set(items[i], record, isRecording);
    }
  },

  drawData(list, sensor, data) {
    const items = Headset.getBySensorAll(list, sensor);
    for (let i = 0; i < items.length; i += 1) {
      Headset.drawData(items[i], data);
    }
  },

  getAll(container = document.body) {
    return container.querySelectorAll('.headsets-list');
  },
};

const RecordItem = {
  create(record) {
    const item = document.createElement('tr');
    item.setAttribute('data-record', record.id);
    this.set(item, record);
    return item;
  },

  set(item, record) {
    const dom = item;
    dom.innerHTML = `<td>${record.id}</td>
      <td>${record.StartTime}</td>
      <td>${record.StopTime}</td>
      <td>${record.ObservationMedia1}</td>
      <td>${record.ObservationMedia2}</td>
      <td>
      <a href="/lablog/record/${record.id}">View</a>, 
      <a class="text-danger" href="/lablog/record/${record.id}/delete/">Delete</a>
      </td>`;
  },

  getByRecordID(container = document.body, id) {
    return container.querySelectorAll(`tr[data-record="${id}"]`);
  },
};

const RecordList = {
  addRecord(list, record) {
    list.appendChild(RecordItem.create(record));
  },
  setRecord(list, record) {
    const items = RecordItem.getByRecordID(list, record.id);
    for (let i = 0; i < items.length; i += 1) {
      RecordItem.set(items[i], record);
    }
  },
  getByExperimentID(container = document.body, id) {
    return container.querySelectorAll(`.js-records-table[data-experiment="${id}"]`);
  },
  getAll(container = document.body) {
    return container.querySelectorAll('.js-records-table');
  },
};

function onAddRecord(data) {
  const lists = RecordList.getByExperimentID(document.body, data.experiment);
  for (let i = 0; i < lists.length; i += 1) {
    RecordList.addRecord(lists[i], data.record);
  }
}

function onUpdateRecord(data) {
  const lists = RecordList.getAll();
  for (let i = 0; i < lists.length; i += 1) {
    RecordList.setRecord(lists[i], data.record);
  }
}

function onAddSensor(data) {
  const lists = HeadsetList.getAll();
  for (let i = 0; i < lists.length; i += 1) {
    HeadsetList.addHeadset(lists[i], data.sensor, data.record, data.is_recorded);
  }
}

function onRemoveSensor(data) {
  const lists = HeadsetList.getAll();
  for (let i = 0; i < lists.length; i += 1) {
    HeadsetList.removeHeadset(lists[i], data.sensor);
  }
}

function onUpdateSensor(data) {
  const lists = HeadsetList.getAll();
  for (let i = 0; i < lists.length; i += 1) {
    HeadsetList.setHeadset(lists[i], data.sensor, data.record, data.is_recorded);
  }
}

function onRawData(data) {
  const lists = HeadsetList.getAll();
  for (let i = 0; i < lists.length; i += 1) {
    HeadsetList.drawData(lists[i], data.sensor, data.data);
  }
}

const WebAPI = {
  init(host) {
    this.socket = new WebSocket(`ws://${host}/ws/api`);
    this.socket.onmessage = function parseMessage(e) {
      const data = JSON.parse(e.data);
      switch (data.command) {
        case 'add_sensor':
          onAddSensor(data);
          break;
        case 'remove_sensor':
          onRemoveSensor(data);
          break;
        case 'update_sensor':
          onUpdateSensor(data);
          break;
        case 'add_record':
          onAddRecord(data);
          break;
        case 'update_record':
          onUpdateRecord(data);
          break;
        case 'raw_sensor':
          onRawData(data);
          break;
        default:
          throw new Error('Unknown command');
      }
    };

    this.socket.onclose = function socketError() {
      throw new Error('WebAPI socket closed unexpectedly');
    };
  },

  startRecording(sensor, experiment) {
    this.socket.send(JSON.stringify({
      command: 'start_recording',
      channel: sensor,
      experiment,
    }));
  },

  stopRecording(sensor, record) {
    this.socket.send(JSON.stringify({
      command: 'stop_recording',
      channel: sensor,
      record,
    }));
  },
};

WebAPI.init(window.location.host);
