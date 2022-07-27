from django.urls import path

from channel import consumer

websocket_urlpatterns = [
    path('ws/sc/<str:channel_name>/', consumer.SyncWebsocketConsumers.as_asgi()),
    path('ws/ac/<str:channel_name>/', consumer.JsonAsyncWebsocketConsumers.as_asgi())
]
