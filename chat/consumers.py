from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async
from asgiref.sync import async_to_sync, sync_to_async
from .models import PrivateChat, Message
from user.models import User
from notification.models import Notification
from django.db.models import Q


class ChatConsumer(AsyncJsonWebsocketConsumer):
    
    async def connect(self):
        self.me = self.scope.get('user')

        await self.accept()
        self.other_username = self.scope['url_route']['kwargs']['username']
        self.user2 = await sync_to_async(User.objects.get)(username=self.other_username)
        self.private_room = await sync_to_async(PrivateChat.objects.create_room_if_none)(self.me, self.user2)
        self.room_name = f'private_room_{self.private_room.id}'
        # print('private room is ', self.private_room.id)
        # print('room is ',self.room_name)
        
        
        await sync_to_async(self.private_room.connect_or_leave)(self.me)

        await self.channel_layer.group_add(
            self.room_name,
            self.channel_name
        )
    

    async def receive_json(self, content):
        command = content.get("command", None)
        print('comd is ',command)
        if command == "private_chat":
            message = content.get("message", None)
            self.newmsg = await sync_to_async(Message.objects.create)(
                room=self.private_room,
                sender=self.me,
                text=message
            )
            created_time = self.newmsg.created_at.strftime("%H:%M %p")
            await self.channel_layer.group_send(
                self.room_name,
                {
                    "type": "websocket_message",
                    "text": message,
                    "created_at":created_time,
                    "id": self.newmsg.id,
                    "username": self.newmsg.sender.username,
                    "avatar": self.newmsg.sender.avatar.url,
                    "command": command
                }
            )

    async def websocket_message(self, event):

        await self.send_json(({
            'id': event["id"],
            'text': event["text"],
            'created_at':event["created_at"],
            'command': event["command"],
            'sender': {
                "username": event["username"],
                "avatar": event["avatar"],
            }
        }))
        

    async def disconnect(self, close_code):
       
        await sync_to_async(self.private_room.connect_or_leave)(self.me)
        await self.channel_layer.group_discard(
            self.room_name,
            self.channel_name
        )
    