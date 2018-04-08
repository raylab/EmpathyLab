from channels.generic.websocket import WebsocketConsumer


class SensorsConsumer(WebsocketConsumer):
    """
    Receives data from headsets
    """

    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        print(text_data)

    def sensors_start_recording(self, event):
        print('SensorsConsumer.start_recording', event)

    def sensors_stop_recording(self, event):
        print('SensorsConsumer.stop_recording', event)
