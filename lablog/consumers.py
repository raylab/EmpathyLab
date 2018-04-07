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
