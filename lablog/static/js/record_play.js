//console.log("ON LOAD:");
//console.log(window.location.pathname);

var errorElm = document.getElementById('error');
var dbFileElm = document.getElementById('dbfile');
var cardHeader = document.getElementsByClassName('card-header');



// Performance measurement functions
var tictime;
if (!window.performance || !performance.now) {window.performance = {now:Date.now}}
function tic () {tictime = performance.now()}
function toc(msg) {
	var dt = performance.now()-tictime;
	console.log((msg||'toc') + ": " + dt + "ms");
}

var myDb = dbFileElm.textContent;
var xhr = new XMLHttpRequest();
xhr.open('GET', '/../static/eeg/' + myDb, true);
xhr.responseType = 'arraybuffer';

var db = {};

xhr.onload = function() {
  //console.log("LOADING");
  var uInt8Array = new Uint8Array(this.response);
  db = new SQL.Database(uInt8Array);
  readDB();
};

var tables = ['Bands', 'Emostate', 'EQ', 'Frames']
//var header = {};
var myRows = [];
var myVar = {};

function readDB() {
	var dumpTable = db.exec("SELECT * FROM dump");
    header = dumpTable[0].columns;
	dumpTable = db.exec("SELECT ID FROM dump");
    for (let i = 0; i < dumpTable[0].values.length; i += 1) { //table run through the rows:
        myRows.push(dumpTable[0].values[i][0])
	}
	//console.log("DONE DUMP:");
	//console.log("columns:" + dumpTable[0].columns.length + "rows:" + myRows);
	myVar = setInterval(myTimer, 250);
};

function doDBRow(){
    var header = {};
    var wsPacket = {};
    wsPacket["Type"] = 'epoc_raw_buffer';
    var currentRow = myRows.shift();
    var newHeader = db.exec("SELECT * FROM dump WHERE ID=" + currentRow);
    for(let i = 0; i < newHeader[0].columns.length; i += 1){
    	wsPacket[newHeader[0].columns[i]] = newHeader[0].values[0][i];
    }
    for (let x = 0; x < tables.length; x += 1){
       	var table = tables[x];
	   	var dumpNum = "SELECT * FROM " + table + " WHERE DUMP_ID=" + currentRow; 
    	var tableData = db.exec(dumpNum);
    	var tableHeader = tableData[0].columns;;
	   	if (table == 'Frames'){ //(tableData[0].values.length > 1){
	  		var tableJSON = [];
	  		for (let y = 0; y < tableData[0].values.length; y += 1) {
	 			var rowJSON = {};
	 			for (let u = 0; u < tableData[0].columns.length; u += 1) {
	 	 			rowJSON[tableData[0].columns[u]] = tableData[0].values[y][u];
	 	   	    }
                tableJSON.push(rowJSON);
	 	  	}
            wsPacket[table] = tableJSON;
        }else if(table == 'Bands'){
        	var tableJSON = [];
        	var el = 0;
        	var trodeJSON = {};
        	for (let bn = 1; bn < tableData[0].columns.length; bn += 1){
        		if (el < 4){
        			var trN = tableData[0].columns[bn].substr(0, tableData[0].columns[bn].lastIndexOf("_"));
        			var trB = tableData[0].columns[bn].substr((tableData[0].columns[bn].lastIndexOf("_") + 1));
        			trodeJSON[trB] = tableData[0].values[0][bn]
        			el += 1;
        	    }else if (el === 4){
        	    	var tpackJSON = {};
        	    	tpackJSON[trN] = trodeJSON;
        	    	tableJSON.push(tpackJSON);
        	    	trodeJSON = {};
        	    	el = 0;
        	    }
        	}    
        	wsPacket[table] = tableJSON;
	 	}else if(table == 'Emostate'){
	 	   	var esColumns = tableData[0].columns;
	 	   	var esData = tableData[0].values[0];
	 	   	var t = esColumns.shift();
	 	   	t = esData.shift();
	 	   	var emoSt = {};
	 	   	for(let ec = 0; ec < 5; ec += 1){
	 	   		var myEs = esColumns.splice(0, 4);
	 	   		var myEm = esData.splice(0, 4);
	 	   		var emName = myEs[0].split("_")[0];
	 	   		var seParm = {};
	 	   	    for(let pc = 0; pc < 4; pc += 1){
	 	   		 	seParm[myEs[pc].split("_")[1]] = myEm[pc];
	 	   		 }
	 	   		emoSt[emName] = seParm;
	 	   	}
	 	   	wsPacket[table] = emoSt;
	 	}else if (tableData[0].values.length == 1) {
	 	   		var rowJSON = {};
	 	   		for (let u = 1; u < tableData[0].columns.length; u += 1) {
	      	        rowJSON[tableData[0].columns[u]] = tableData[0].values[0][u];
	            };
	            //console.log("SINGLE ROW")
	            wsPacket[table] = rowJSON;
	 	}
    }
    //console.log("WOULD SEND THIS TO WS:");
    //console.log(JSON.stringify(wsPacket));
    $('.progress-through-file')[0].innerHTML = "Frames remain: " + myRows.length
	SensorSimAPI.pushJSONPacket(JSON.stringify(wsPacket));
};

function myTimer() {
    if (myRows.length == 0){
    	//console.log("DONE");
    	clearInterval(myVar);
    	rptBtn.textContent = 'play';
    }else{
    	doDBRow();
    }
}

xhr.send();


const RepeatButton = {
  create() {
    const btn = document.createElement('button');
    this.set(btn);
    return btn;
  },
  set(btn) {
    const dom = btn;
    dom.className = 'js-play-button btn btn-sm';
    dom.textContent = 'pause';//isRecording ? 'Stop' : 'Record';
    //dom.setAttribute('data-active', isRecording);
    //dom.setAttribute('subject-id', 'none');
  },
  getAll(container = document.body) {
    return container.querySelectorAll('.js-play-button');
  },
};

//console.log("MAKING A BUTTON")
//console.log(cardHeader);
var rptBtn = RepeatButton.create();
//cardHeader[0].appendChild(rpt.rptBtn);

rptBtn.addEventListener('click', () => {
    if (myRows.length == 0) {
        rptBtn.textContent = 'pause';
        readDB();
    } else if (myRows.length != 0){
    	if(rptBtn.textContent == 'pause'){
    		clearInterval(myVar);
    		rptBtn.textContent = 'play';
    	}else if(rptBtn.textContent == 'play'){
    		myVar = setInterval(myTimer, 250);
    		rptBtn.textContent = 'pause';
    	}
    	
//          item.dispatchEvent(new CustomEvent('startRecording'));
    }
});

cardHeader[0].appendChild(rptBtn);
const fileLength = document.createElement('div');
fileLength.className = 'progress-through-file';
cardHeader[0].appendChild(fileLength);



const SensorSimAPI = {
  init(host) {
    this.socket = new WebSocket(`ws://${host}/ws/sensors`);
    this.socket.onclose = function socketError() {
      throw new Error('WebAPI socket closed unexpectedly');
    };
  },

  pushJSONPacket(JSONPacket) {
  	this.socket.send(JSONPacket);
  },
};

SensorSimAPI.init(window.location.host);