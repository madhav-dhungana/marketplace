from .consumers import ChatConsumer
from django.urls import path

chat_ws_urlpatterns=[
    path('ws/chat/<str:username>/',ChatConsumer.as_asgi())
]