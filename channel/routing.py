from django.urls import path

from channel import consumer

websocket_urlpatterns = [
    path('ws/sc/', consumer.MyConsumer.as_asgi()),
    path('ws/ac/', consumer.MyAsyncConsumer.as_asgi())
]
