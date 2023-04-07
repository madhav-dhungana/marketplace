from .consumers import NotifyConsumer
from django.urls import path

notification_urlpatterns=[
    # path('ws/clicked/<room_name>/',BingoConsumer.as_asgi(),name="clicked"),
    path('ws/notification/',NotifyConsumer.as_asgi())
]