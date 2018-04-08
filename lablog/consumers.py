from channels.generic.websocket import WebsocketConsumer, JsonWebsocketConsumer
from asgiref.sync import async_to_sync


class SensorsConsumer(WebsocketConsumer):
    """
    Receives data from headsets
    """

    def connect(self):
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

    def receive(self, text_data):
        print(text_data)

    def sensors_start_recording(self, event):
        print('SensorsConsumer.start_recording', event)

    def sensors_stop_recording(self, event):
        print('SensorsConsumer.stop_recording', event)

    def sensors_ping(self, event):
        async_to_sync(self.channel_layer.send)(
            event["respond_channel"],
            {
                "type": "webui.add_sensor",
                "channel": self.channel_name,
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
        print(content)
        if content['command'] == 'start_recording':
            async_to_sync(self.channel_layer.send)(
                content["channel"],
                {
                    "type": "sensors.start_recording",
                    "channel": self.channel_name,
                },
            )
        elif content['command'] == 'stop_recording':
            async_to_sync(self.channel_layer.send)(
                content["channel"],
                {
                    "type": "sensors.stop_recording",
                    "channel": self.channel_name,
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
            'sensor': event["channel"]
        })

    def webui_remove_sensor(self, event):
        self.send_json({
            'command': 'remove_sensor',
            'sensor': event["channel"]
        })
