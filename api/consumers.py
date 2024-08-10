import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync

class LogConsumer(WebsocketConsumer):
    def connect(self):
        self.group_name = "log_group"
        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name
        )
        self.accept()
        print("WebSocket connected")

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name,
            self.channel_name
        )
        print(f"WebSocket disconnected with code: {close_code}")

    def receive(self, text_data):
        print(f"Received message: {text_data}")
        self.send(text_data=json.dumps({
            'message': f"Server received: {text_data}"
        }))

    def send_log_update(self, event):
        log_entry = event['log_entry']
        self.send(text_data=json.dumps({
            'log': log_entry
        }))