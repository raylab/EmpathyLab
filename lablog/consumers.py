from channels.generic.websocket import JsonWebsocketConsumer
from django.template import defaultfilters
from asgiref.sync import async_to_sync
from lablog.models import Record, Experiment
from datetime import datetime, timezone
from lablog import eeg
from django.conf import settings


class SensorsConsumer(JsonWebsocketConsumer):
    """
    Receives data from headsets
    """

    def connect(self):
        self.is_recorded = False
        self.record = 0
        async_to_sync(
            self.channel_layer.group_add)(
            "sensors",
            self.channel_name)
        self.accept()
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

    def receive_json(self, content):
        async_to_sync(self.channel_layer.group_send)(
            "webui",
            {
                "type": "webui.raw_sensor",
                "channel": self.channel_name,
                "data": content
            },
        )
        if self.is_recorded:
            self.eeg.append_json(content)

    def sensors_start_recording(self, event):
        if not self.is_recorded:
            self.experiment = Experiment.objects.get(id=event["experiment"])
            self.eeg = eeg.Data(settings.EEGDATA_STORE_PATH)
            record_obj = Record.objects.create(
                StartTime=datetime.now(tz=timezone.utc), EEG=self.eeg.filename)
            record_obj.save()
            self.experiment.records.add(record_obj)
            self.record = record_obj.id
            self.is_recorded = True
            self.sensors_update()
            self.sensors_add_record(self.experiment, record_obj)

    def sensors_stop_recording(self, event):
        if self.is_recorded:
            self.is_recorded = False
            record_obj = Record.objects.get(pk=self.record)
            record_obj.StopTime = datetime.now(tz=timezone.utc)
            record_obj.save()
            self.sensors_update_record(self.experiment, record_obj)
            self.eeg = None
            self.experiment = None
            self.record = 0
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

    def sensors_add_record(self, experiment, record):
        async_to_sync(
            self.channel_layer.group_send)(
            "webui",
            {"type": "webui.add_record", "channel": self.channel_name,
             "experiment": experiment.id, "record_id": record.id,
             "record_StartTime": defaultfilters.date(
                 record.StartTime, "DATETIME_FORMAT"),
             "record_StopTime": "",
             "record_ObservationMedia1": record.ObservationMedia1,
             "record_ObservationMedia2": record.ObservationMedia2, },)

    def sensors_update_record(self, experiment, record):
        async_to_sync(
            self.channel_layer.group_send)(
            "webui",
            {"type": "webui.update_record", "channel": self.channel_name,
             "experiment": experiment.id, "record_id": record.id,
             "record_StartTime": defaultfilters.date(
                 record.StartTime, "DATETIME_FORMAT"),
             "record_StopTime": defaultfilters.date(
                 record.StopTime, "DATETIME_FORMAT"),
             "record_ObservationMedia1": record.ObservationMedia1,
             "record_ObservationMedia2": record.ObservationMedia2, },)

    def sensors_ping(self, event):
        async_to_sync(self.channel_layer.send)(
            event["respond_channel"],
            {
                "type": "webui.add_sensor",
                "channel": self.channel_name,
                "is_recorded": self.is_recorded,
                "record": self.record,
            },
        )


class WebAPIConsumer(JsonWebsocketConsumer):
    """
    Communicates with client-side script
    """

    def connect(self):
        async_to_sync(self.channel_layer.group_add)("webui", self.channel_name)
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

    def receive_json(self, content):
        if content['command'] == 'start_recording':
            async_to_sync(self.channel_layer.send)(
                content["channel"],
                {
                    "type": "sensors.start_recording",
                    "channel": self.channel_name,
                    "experiment": content["experiment"],
                },
            )
        elif content['command'] == 'stop_recording':
            async_to_sync(self.channel_layer.send)(
                content["channel"],
                {
                    "type": "sensors.stop_recording",
                    "channel": self.channel_name,
                    "record": content["record"],
                },
            )
        else:
            self.send_json({
                'command': 'error_command',
                'message': 'Unrecognized command'
            })

    def webui_add_sensor(self, event):
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
        self.send_json({
            'command': 'update_sensor',
            'sensor': event["channel"],
            'is_recorded': event["is_recorded"],
            'record': event["record"],
        })

    def webui_add_record(self, event):
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
            'experiment': event["experiment"],
            'record': {
                'id': event["record_id"],
                'StartTime': event["record_StartTime"],
                'StopTime': event["record_StopTime"],
                'ObservationMedia1': event['record_ObservationMedia1'],
                'ObservationMedia2': event['record_ObservationMedia2']
            }
        })

    def webui_raw_sensor(self, event):
        self.send_json({
            'command': 'raw_sensor',
            'sensor': event["channel"],
            'data': event["data"]
        })
