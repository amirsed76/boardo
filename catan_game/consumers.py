import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from . import models


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        # try:
        #     players_id = [x["player"] for x in models.PlayerGame.objects.filter(
        #         catan_event__event__room_name=self.room_name).values(
        #         "player")]
        #
        #     if self.scope["user"].id in players_id:
        #         self.accept()
        # except:
        #     pass

        self.accept()
    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

        # Receive message from room group

    # def chat_message(self, event):
    #     message = event['message']
    #
    #     # Send message to WebSocket
    #
    #     self.send(text_data=json.dumps({
    #         'message': message
    #     }))

    def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket

        self.send(text_data=json.dumps({
            'message': message
        }))
