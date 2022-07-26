from django.urls import path

from channel import consumer

websocket_urlpatterns = [
    path('ws/sc/', consumer.SyncWebsocketConsumers.as_asgi()),
    path('ws/ac/', consumer.AsyncWebsocketConsumers.as_asgi())
]
