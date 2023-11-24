from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from django.utils.timesince import timesince

from .models import ChatRoom, Message
from django.contrib.auth.models import User

from .templatetags.chatextras import initials

import json

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.chatroom_name = self.scope['url_route']['kwargs']['room_id']
        self.chatroom_group_name = f'chat_{self.chatroom_name}'
        self.user = self.scope['user']

        #join room group
        await self.get_chatroom()
        await self.channel_layer.group_add(self.chatroom_group_name, self.channel_name)
        await self.accept()

        #inform client about joining chat


    async def disconnect(self, close_code):
        #Leave room
        await self.channel_layer.group_discard(self.chatroom_group_name, self.channel_name)


    async def receive(self, text_data):
        #Receive message from websocket(frontend)
        text_data_json = json.loads(text_data)

        type = text_data_json['type']
        message = text_data_json.get('message', '')
        name = text_data_json.get('name', '')
        user_id = text_data_json.get('user_id', '')

        print('Receive:', type)

        if type == 'message':
            new_message = await self.create_message(message, user_id)

            # send message to group/ room
            await self.channel_layer.group_send(self.chatroom_group_name, {
                'type': 'chat_message',
                'message': message,
                'name': name,
                'initials': initials(name),
                'user_id': user_id,
                'created_at': timesince(new_message.created_at)
            })
        elif type == 'writing_on':
            # send message to group/ room
            await self.channel_layer.group_send(self.chatroom_group_name, {
                'type': 'add_writing_status',
                'message': message,
                'name': name,
                'initials': initials(name),
                'user_id': user_id,
            })
        elif type == 'writing_off':
            # send message to group/ room
            await self.channel_layer.group_send(self.chatroom_group_name, {
                'type': 'remove_writing_status',
            })

    
    async def chat_message(self, event):
        # Send message to WebSocket (front end)
        await self.send(text_data=json.dumps({
            'type': event['type'],
            'message': event['message'],
            'name': event['name'],
            'initials': event['initials'],
            'user_id': event['user_id'],
            'created_at': event['created_at'],
        }))


    async def add_writing_status(self, event):
        # Send message to WebSocket (front end)
        await self.send(text_data=json.dumps({
            'type': event['type'],
            'message': event['message'],
            'name': event['name'],
            'initials': event['initials'],
            'user_id': event['user_id'],
        }))


    async def remove_writing_status(self, event):
        # Send message to WebSocket (front end)
        await self.send(text_data=json.dumps({
            'type': event['type']
        }))



    @sync_to_async
    def get_chatroom(self):
        self.chatroom = ChatRoom.objects.get(id=self.chatroom_name)

    @sync_to_async
    def create_message(self, message, user_id):
        message = Message.objects.create(body=message)
        message.sent_by = User.objects.get(pk=user_id)
        message.save()

        self.chatroom.messages.add(message)

        return message