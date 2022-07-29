from django.urls import path

from channel import consumer

websocket_urlpatterns = [
    path('ws/ac/', consumer.JsonAsyncWebsocketConsumers.as_asgi())
]
