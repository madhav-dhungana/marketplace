# from .consumers import BingoConsumer, OnlineRoomConsumer
from django.urls import path
from notification.routing import notification_urlpatterns
from chat.routing import chat_ws_urlpatterns

websocket_urlpatterns=[]

websocket_urlpatterns+=notification_urlpatterns+chat_ws_urlpatterns