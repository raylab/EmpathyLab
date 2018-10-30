from channels.generic.websocket import WebsocketConsumer, JsonWebsocketConsumer, AsyncJsonWebsocketConsumer
from channels.consumer import SyncConsumer
from django.template import defaultfilters
from asgiref.sync import async_to_sync
from lablog.models import Record, Experiment
from datetime import datetime, timezone
from lablog import eeg
from django.conf import settings
from datetime import datetime


class SensorsConsumer(JsonWebsocketConsumer):
    """
    Receives data from headsets
    """

    def connect(self):
        self.id = 0
        self.is_recorded = False
        self.analysis = None
        self.analysis_id = None
        self.record = None
        self.eeg_filename = None

        async_to_sync(
            self.channel_layer.group_add)(
            "sensors",
            self.channel_name)
        self.accept()
        #print("Sensor connect:")
        async_to_sync(self.channel_layer.group_send)(
            "webui",
            {
                "type": "webui.add_sensor",
                "channel": self.channel_name,
                "is_recorded": self.is_recorded,
                "record": self.record,
            },
        )

    def disconnect(self, close_code):
        async_to_sync(
            self.channel_layer.group_discard)(
            "sensors",
            self.channel_name)
        async_to_sync(self.channel_layer.group_send)(
            "webui",
            {
                "type": "webui.remove_sensor",
                "channel": self.channel_name,
            },
        )

    def receive_json(self, data):
        self.id += 1
        data["ID"] = self.id
        data["TIMESTAMP"] = str(datetime.now())
        #print("Got DATA:"+data['RecordNumber']) #Getting raw data from Harvister
        if self.eeg_filename:
            data["record_filename"] = self.eeg_filename
            data["tnes"] = self.analysis
            eeg.add_eeg(data["record_filename"], data)

        async_to_sync(self.channel_layer.group_send)(
            "raw",
            {
                "type": "raw.sensor",
                "channel": self.channel_name,
                "data": data
            },
        )

    def sensors_start_recording(self, event):
        self.eeg_filename = event["eeg_filename"]
        self.record = event["record"]
        self.analysis_id = event["analysis_id"]
        self.analysis = event["analysis"]
        self.is_recorded = True
        self.sensors_update()

    def sensors_stop_recording(self, event):
        self.is_recorded = False
        self.analysis = None
        self.analysis_id = None
        self.record = None
        self.eeg_filename = None
        self.sensors_update()

    def sensors_update(self):
        async_to_sync(self.channel_layer.group_send)(
            "webui",
            {
                "type": "webui.update_sensor",
                "channel": self.channel_name,
                "is_recorded": self.is_recorded,
                "record": self.record,
            },
        )

    def sensors_ping(self, event):
        #print("Sensor ping:"+str(event))
        async_to_sync(self.channel_layer.send)(
            event["respond_channel"],
            {
                "type": "webui.add_sensor",
                "channel": self.channel_name,
                "is_recorded": self.is_recorded,
                "record": self.record,
            },
        )

    def sensors_update_analysis(self, event):
        if self.is_recorded and self.analysis_id == event["id"]:
            self.analysis = event["analysis"]


class WebAPIConsumer(JsonWebsocketConsumer):
    """
    Communicates with client-side script
    """
    def connect(self):
        self.headset_name = None

        async_to_sync(self.channel_layer.group_add)("webui", self.channel_name)
        async_to_sync(self.channel_layer.group_add)("raw", self.channel_name)
        self.accept()       
        async_to_sync(self.channel_layer.group_send)(
            "sensors",
            {
                "type": "sensors.ping",
                "respond_channel": self.channel_name,
            },
        )

    def disconnect(self, close_code):
        async_to_sync(
            self.channel_layer.group_discard)(
            "webui", self.channel_name)
        async_to_sync(
            self.channel_layer.group_discard)(
            "raw", self.channel_name)

    def start_recording(self, channel, experiment_id, subject_id):
        #print("START RECORD:", channel, experiment_id, subject_id)
        #eeg_filename = str(eeg.generate_name())#FileName will be same as Record Number 
        eeg_filename = str(eeg.generate_name(self.headset_name))#in the EPOC Hartvister with timestamp
        start = datetime.now(tz=timezone.utc)  
        myExpr = Experiment.objects.filter(id=experiment_id).values()[0] 
        record = Record.objects.create(StartTime=start, EEG=eeg_filename, ExperimentId_id=experiment_id , SubjectId_id=subject_id)
        record.save()
        experiment = Experiment.objects.get(id=experiment_id)
        experiment.records.add(record)
        async_to_sync(self.channel_layer.group_send)(
            "webui",
            {
                "type": "webui.add_record",
                "experiment": experiment_id, "record_id": record.id,
                "record_StartTime": defaultfilters.date(
                        record.StartTime, "DATETIME_FORMAT"),
                "record_StopTime": "",
                "record_ObservationMedia1": record.ObservationMedia1,
                "record_ObservationMedia2": record.ObservationMedia2
            }
        )
        analysis = experiment.feedback.analysis
        analysis_id = analysis.id
        analysis_values = {
            "A": analysis.A,
            "B": analysis.B,
            "C": analysis.C,
            "D": analysis.D,
            "H": analysis.H,
            "L": analysis.L
        }
        async_to_sync(self.channel_layer.send)(
            channel,
            {
                "type": "sensors.start_recording",
                "channel": self.channel_name,
                "eeg_filename": eeg_filename,
                "record": record.id,
                "analysis_id": analysis_id,
                "analysis": analysis_values
            },
        )

    def stop_recording(self, channel, record_id):
        async_to_sync(self.channel_layer.send)(
            channel,
            {
                "type": "sensors.stop_recording",
                "channel": self.channel_name,
                "record": record_id,
            },
        )
        record = Record.objects.get(pk=record_id)
        record.StopTime = datetime.now(tz=timezone.utc)
        record.save()
        async_to_sync(
            self.channel_layer.group_send)(
            "webui",
            {
                "type": "webui.update_record",
                "record": {
                    "id": record.id,
                    "StartTime": defaultfilters.date(
                        record.StartTime,
                        "DATETIME_FORMAT"),
                    "StopTime": defaultfilters.date(
                        record.StopTime,
                        "DATETIME_FORMAT"),
                    "ObservationMedia1": record.ObservationMedia1,
                    "ObservationMedia2": record.ObservationMedia2}})

    def receive_json(self, content):
        cmd = content['command']
        channel = content['channel']
        #Recording commands from GUI
        print("WEBUI recieve_json:"+ str(content))
        if cmd == 'start_recording':
            self.start_recording(channel, content["experiment"], content["subjectId"])
        elif cmd == 'stop_recording':
            self.stop_recording(channel, content["record"])
        else:
            self.send_json({
                'command': 'error_command',
                'message': 'Unrecognized command'
            })

    def webui_add_sensor(self, event):
        #print("WEBUI add_sensor:"+str(event))
        self.send_json({
            'command': 'add_sensor',
            'sensor': event["channel"],
            'is_recorded': event["is_recorded"],
            'record': event["record"],
        })

    def webui_remove_sensor(self, event):
        self.send_json({
            'command': 'remove_sensor',
            'sensor': event["channel"]
        })

    def webui_update_sensor(self, event):
        #print("WEBUI update_sensor:"+str(event))
        self.send_json({
            'command': 'update_sensor',
            'sensor': event["channel"],
            'is_recorded': event["is_recorded"],
            'record': event["record"],
        })

    def webui_add_record(self, event):
        #print("WEB UI Add Record")
        self.send_json({
            'command': 'add_record',
            'experiment': event["experiment"],
            'record': {
                'id': event["record_id"],
                'StartTime': event["record_StartTime"],
                'StopTime': event["record_StopTime"],
                'ObservationMedia1': event['record_ObservationMedia1'],
                'ObservationMedia2': event['record_ObservationMedia2']
            }
        })

    def webui_update_record(self, event):
        self.send_json({
            'command': 'update_record',
            'record': event['record'],
        })

    def raw_sensor(self, event): #Here raw json from sensor get's into the WebAPI
        #print("Here:"+ str(event["data"]))
        self.headset_name = event["data"]['RecordNumber'] #Here we catching Record Number from the EPOC
        self.send_json({                                  #Harvister and storing it.
            'command': 'raw_sensor',
            'sensor': event["channel"],
            'data': event["data"]
        })


class TNESConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.sensor = self.scope['url_route']['kwargs']['sensor']
        await self.channel_layer.group_add("tnes", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("tnes", self.channel_name)

    async def raw_sensor(self, event):
        if event["data"]["RecordNumber"] == self.sensor and "tnes" in event["data"]:
            await self.send_json(event["data"]["tnes"])


class PublicConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.sensor = self.scope['url_route']['kwargs']['sensor']
        await self.channel_layer.group_add("raw", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("raw", self.channel_name)

    async def raw_sensor(self, event):
        if event["data"]["RecordNumber"] == self.sensor:
            await self.send_json(event["data"])


class AnalyzercConsumer(JsonWebsocketConsumer):
    def connect(self):
        self.sensor = self.scope['url_route']['kwargs']['sensor']
        async_to_sync(
            self.channel_layer.group_add)(
            "raw",
            self.channel_name)
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(
            self.channel_layer.group_discard)(
            "raw",
            self.channel_name)

    def raw_sensor(self, event):
        if event["data"]["RecordNumber"] == self.sensor:
            self.send_json(event["data"])

    def receive_json(self, data):
        eeg.add_tnes(data["record_filename"], data)
        async_to_sync(self.channel_layer.group_send)(
            "tnes",
            {
                "type": "raw.sensor",
                "channel": self.sensor,
                "data": data
            },
        )
