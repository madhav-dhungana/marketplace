
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async
from asgiref.sync import async_to_sync, sync_to_async
import json
from .models import Notification

class NotifyConsumer(AsyncJsonWebsocketConsumer):

    async def connect(self):
        # self.url_route = self.scope['url_route']['kwargs']['room_name']
        self.me = self.scope.get('user').username
        await self.accept()
        self.room_name = f'notify_{self.me}'
        await self.channel_layer.group_add(
            self.room_name,
            self.channel_name
        )

    async def receive_json(self,content,**kwargs):
        return await super().receive_json(content, **kwargs)
    

    async def send_notification(self, event):
        await self.send_json(({
            'message': event["message"],
            'count': event["count"],
            'time': event["time"],
            "action_by_url":event["action_by_url"],
            "notification_url":event["notification_url"],
        }))

    async def disconnect(self,close_code):
        print('disconnected')
        await self.channel_layer.group_discard(
            self.room_name,
            self.channel_name
        )