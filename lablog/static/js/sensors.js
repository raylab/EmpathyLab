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
    dom.setAttribute('subject-id', 'none');
  },
  getAll(container = document.body) {
    return container.querySelectorAll('.js-record-button');
  },
};


const SubjectSelector = {
  create(experimentID) {
    const item = document.createElement('select', {passive: true});
    item.setAttribute('id', 'subject-select');
    var myElement = document.getElementsByClassName("divsubject");
    for (let i = 0; i < myElement.length; i += 1) {
      subjId = document.createElement('option');
      subjId.setAttribute('value', myElement[i].innerText);
      t = document.createTextNode(myElement[i].innerText);
      subjId.appendChild(t);
      item.appendChild(subjId); 
    }
    return item;
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
  EQ:{},
  create(sensor) {
    const chart = document.createElement('canvas');
    chart.height = 430;
    chart.width = 600;
    chart.className = 'js-sensors-chart';
    this.queues[sensor] = [];
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

        if (i > 40 && tOld != ((tNew - 1) % 256)) {//Left edge of the time grid 140
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
        ctx.fillText(this.header[chan], 15, y);//Position of the electrode name
        ctx.beginPath();
        ctx.strokeStyle = 'rgb(255,255,255)';
        const initial = frames[cnt - 1][this.header[chan]];
        ctx.moveTo(x, y + (initial - 4200) * 0.5);
        for (let i = cnt - 1; i >= 0; i -= 1) {
          const frame = frames[i];
          const value = frame[this.header[chan]];
          ctx.lineTo(x--, y + (value - 4200) * 0.5);
          if (x === 40) { break; }//Left edge oh the electrode graph 40
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

        if (i > 40 && Math.floor(tNew) !== Math.floor(tOld)) { //Left edge of the time grid 40
          ctx.beginPath();
          ctx.moveTo(i, 20);
          ctx.lineTo(i, chart.height - 60);
          ctx.stroke();
          ctx.fillText(Math.floor(tNew), i - 8, 16);
        }
      }
    }
  },
  draw(chart, frames, emostate = null, EQ = null) {
    const ctx = chart.getContext('2d');
    //console.log("CHART");
    //console.log(ctx);//.clientWidth);
    let foo = document.getElementById('dash-table').rows[0].cells[1].clientWidth; //[1].offsetWidth;
    //console.log(foo);//[1].clientWidth);
    //console.log(chart.width);
    chart.width = (foo - 5);
    ctx.fillStyle = 'black';
    ctx.fillRect(0, 0, chart.width, chart.height);
    this.drawTimeGrid(chart, frames);
    this.drawElectrodeData(chart, frames);
    this.drawDroppedPackets(chart, frames);
    //console.log(EQ);
  },
  getAll(container = document.body) {
    return container.querySelectorAll('.js-sensors-chart');
  },
};


const EQdash = { 
  create(sensor) {
   const chart = document.createElement('canvas');
    chart.height = 431;
    chart.width = 349;
    chart.className = 'js-eq-quality-chart';
    //this.queues[sensor] = [];
    chart.setAttribute('id', 'eq-quality');
    //var myTrode = ['CMS', 'DLR', 'AF3', 'F7', 'F3', 'FC5', 'T7', 'P7', 'O1', 'O2', 'P8', 'T8', 'FC6', 'F4', 'F8', 'AF4'];
    var myElement = document.getElementsByClassName("eq-quality");
    //console.log("CREATING EQ DASH");
    return chart;

  },
  draw(chart, EQ){
    const ctx = chart.getContext('2d');
    //ctx.fillStyle = 'grey';
    //ctx.fillRect(0, 0, chart.width, chart.height);
    var BGimageObj = new Image();
    BGimageObj.onload = function(){
    	ctx.drawImage(BGimageObj, 0, 0);
    };
    BGimageObj.src = "/static/res/BG_enames.png";
    var foo = EQ;
    //var myTrode = ['CMS', 'DLR', 'AF3', 'F7', 'F3', 'FC5', 'T7', 'P7', 'O1', 'O2', 'P8', 'T8', 'FC6', 'F4', 'F8', 'AF4'];
    
    var IEE_CHAN_AF3 = new Image();
    IEE_CHAN_AF3.onload = function(){
    	ctx.drawImage(IEE_CHAN_AF3, 85, 60);
    };
    IEE_CHAN_AF3.src = "/static/res/electrode_q" + foo['IEE_CHAN_AF3'] + ".png";

    var IEE_CHAN_AF4 = new Image();
    IEE_CHAN_AF4.onload = function(){
    	ctx.drawImage(IEE_CHAN_AF4, 230, 60);
    };
    IEE_CHAN_AF4.src = "/static/res/electrode_q" + foo['IEE_CHAN_AF4'] + ".png";
    var IEE_CHAN_F7 = new Image();
    IEE_CHAN_F7.onload = function(){
    	ctx.drawImage(IEE_CHAN_F7, 40, 110);
    };
    IEE_CHAN_F7.src = "/static/res/electrode_q" + foo['IEE_CHAN_F7'] + ".png";
    var IEE_CHAN_F8 = new Image();
    IEE_CHAN_F8.onload = function(){
    	ctx.drawImage(IEE_CHAN_F8, 275, 110);
    };
    IEE_CHAN_F8.src = "/static/res/electrode_q" + foo['IEE_CHAN_F8'] + ".png";  
    var IEE_CHAN_F3 = new Image();
    IEE_CHAN_F3.onload = function(){
    	ctx.drawImage(IEE_CHAN_F3, 105, 120);
    };
    IEE_CHAN_F3.src = "/static/res/electrode_q" + foo['IEE_CHAN_F3'] + ".png";
    var IEE_CHAN_F4 = new Image();
    IEE_CHAN_F4.onload = function(){
    	ctx.drawImage(IEE_CHAN_F4, 215, 120);
    };
    IEE_CHAN_F4.src = "/static/res/electrode_q" + foo['IEE_CHAN_F4'] + ".png";
    var IEE_CHAN_FC5 = new Image();
    IEE_CHAN_FC5.onload = function(){
    	ctx.drawImage(IEE_CHAN_FC5, 65, 170);
    };
    IEE_CHAN_FC5.src = "/static/res/electrode_q" + foo['IEE_CHAN_FC5'] + ".png";
    var IEE_CHAN_FC6 = new Image();
    IEE_CHAN_FC6.onload = function(){
    	ctx.drawImage(IEE_CHAN_FC6, 255, 170);
    };
    IEE_CHAN_FC6.src = "/static/res/electrode_q" + foo['IEE_CHAN_FC6'] + ".png";
   var IEE_CHAN_T7 = new Image();
    IEE_CHAN_T7.onload = function(){
    	ctx.drawImage(IEE_CHAN_T7, 20, 210);
    };
    IEE_CHAN_T7.src = "/static/res/electrode_q" + foo['IEE_CHAN_T7'] + ".png";
    var IEE_CHAN_T8 = new Image();
    IEE_CHAN_T8.onload = function(){
    	ctx.drawImage(IEE_CHAN_T8, 295, 210);
    };
    IEE_CHAN_T8.src = "/static/res/electrode_q" + foo['IEE_CHAN_T8'] + ".png";
    var IEE_CHAN_CMS = new Image();
    IEE_CHAN_CMS.onload = function(){
    	ctx.drawImage(IEE_CHAN_CMS, 40, 275);
    };
    IEE_CHAN_CMS.src = "/static/res/relectrode_q" + foo['IEE_CHAN_CMS'] + ".png";
    var IEE_CHAN_DRL = new Image();
    IEE_CHAN_DRL.onload = function(){
    	ctx.drawImage(IEE_CHAN_DRL, 270, 275);
    };
    IEE_CHAN_DRL.src = "/static/res/relectrode_q" + foo['IEE_CHAN_DRL'] + ".png";  
    var IEE_CHAN_P7 = new Image();
    IEE_CHAN_P7.onload = function(){
    	ctx.drawImage(IEE_CHAN_P7, 78, 320);
    };
    IEE_CHAN_P7.src = "/static/res/electrode_q" + foo['IEE_CHAN_P7'] + ".png";

    var IEE_CHAN_P8 = new Image();
    IEE_CHAN_P8.onload = function(){
    	ctx.drawImage(IEE_CHAN_P8, 237, 320);
    };
    IEE_CHAN_P8.src = "/static/res/electrode_q" + foo['IEE_CHAN_P8'] + ".png";
    var IEE_CHAN_O1 = new Image();
    IEE_CHAN_O1.onload = function(){
    	ctx.drawImage(IEE_CHAN_O1, 115, 390);
    };
    IEE_CHAN_O1.src = "/static/res/electrode_q" + foo['IEE_CHAN_O1'] + ".png";
    var IEE_CHAN_O2 = new Image();
    IEE_CHAN_O2.onload = function(){
    	ctx.drawImage(IEE_CHAN_O2, 200, 390);
    };
    IEE_CHAN_O2.src = "/static/res/electrode_q" + foo['IEE_CHAN_O2'] + ".png";
    //console.log("DRAWING EQ");
    //console.log(foo);//['IEE_CHAN_AF3']);//ctx.canvas.baseURI);

  },
  getAll(container = document.body) {
    return container.querySelectorAll('.js-eq-quality-chart');
  },
};

const Headset = {
  create(sensor, record, isRecording, showRecordButton, experimentID) {
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
      const subjSelect = SubjectSelector.create(experimentID);
      subjSelect.addEventListener('click', () => {
          var subjId = subjSelect.options[subjSelect.selectedIndex].value;
          item.setAttribute('subject-id', subjId);
        {passive: true} 
       });
      header.appendChild(subjSelect);
    }
    item.appendChild(header);
    const body = document.createElement('table');
    body.setAttribute('id', 'dash-table');
    var row = body.insertRow(0);
    var cell1 = row.insertCell(0);
    var cell2 = row.insertCell(1);
    cell1.append(EQdash.create(sensor));//This is if we deploy EQ-dash
    cell2.append(Chart.create(sensor));
    cell1.setAttribute('width', "240");
    cell2.setAttribute('width', "100%");
    //console.log("TABLE CELLS")
    item.appendChild(body);
    //item.appendChild(Chart.create(sensor));
    //item.appendChild(EQdash.create(sensor));
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
    const EQchart = EQdash.getAll(item);//If EQ-dash is enabled, uncomment this.
    //console.log(data.Frames); //Get's data from the Headset and draws it.
    //console.log(item);//charts.length);
    for (let i = 0; i < charts.length; i += 1) {
      const frames = Chart.queues[item.getAttribute('data-channel')];
      let emostate = Chart.emostates[item.getAttribute('data-channel')];
      let EQ = Chart.EQ[item.getAttribute('data-channel')];
      Array.prototype.push.apply(frames, data.Frames);
      if (frames.length > charts[i].width) {
        frames.splice(0, frames.length - charts[i].width);
      }
      if ('Emostate' in data) {
        emostate = data.Emostate;
        Chart.emostates[item.getAttribute('data-channel')] = emostate;
        //console.log(Chart.emostates);
      }
      if ('EQ' in data){
      	EQ = data.EQ;
        Chart.EQ[item.getAttribute('data-channel')] = EQ;
      	//console.log("EQ SENT");//data.EQ);
      	//console.log(EQ);
      }
      item.firstChild.firstChild.nodeValue = data.RecordNumber;
      window.requestAnimationFrame(() => {  //Actually sending things..
        Chart.draw(charts[i], frames, emostate, EQ);
        EQdash.draw(EQchart[i], EQ); //If EQ-dash is enabled uncomment this.
      });
    }
  },

  getAll(container = document.body) {
    //console.log("HERE");
    return container.querySelectorAll('.js-headset-item');
  },

  getBySensorAll(container = document.body, sensor) {
    return container.querySelectorAll(`.js-headset-item[data-channel="${sensor}"]`);
  },
};

const HeadsetList = {
  addHeadset(list, sensor, record, isRecording) {
    const showRecordButton = list.hasAttribute('data-allow-recording');
    const experimentID = list.getAttribute('data-experiment');
    const item = Headset.create(sensor, record, isRecording, showRecordButton, experimentID);
    item.addEventListener('startRecording', () => {
      WebAPI.startRecording(sensor, list.getAttribute('data-experiment'), item.getAttribute('subject-id'));
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
    //'Frames' get here...
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
  //console.log("HERE-A:");
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

  startRecording(sensor, experiment, subjectId) {
    //console.log("START RECORDING:" + sensor);
    if (subjectId === null){
        getSubjId = confirm("SET SUBJECT ID");
        return;
    }
    this.socket.send(JSON.stringify({
      command: 'start_recording',
      channel: sensor,
      experiment,
      subjectId,
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
