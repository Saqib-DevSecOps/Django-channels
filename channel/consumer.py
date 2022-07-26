import asyncio
from time import sleep
import json
from asgiref.sync import async_to_sync
from channels.consumer import SyncConsumer, AsyncConsumer
from channels.db import database_sync_to_async
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
# ======================Synchronous Consumer========================================================
from channels.exceptions import StopConsumer

#
# class MyConsumer(SyncConsumer):
#     # This Handler is called when client initially open a connection and is about to finishing handshake
#
#     def websocket_connect(self, event):
#         print('Connection Connected', event)
#         self.send({
#             'type': 'websocket.accept'
#         })
#
#     # This Handler is called When data received from client
#
#     def websocket_receive(self, event):
#         print('Message Received', event['text'])
#
#         for i in range(50):
#             self.send(
#                 dict(type='websocket.send', text=str(i))
#             )
#             sleep(1)
#
#     # This Handler is called when client lost the connection closing the connection the server lose the connection
#
#     def websocket_disconnect(self, event):
#         print('Connection Disconnected', event)
#         raise StopConsumer()
#
#
# # =============================Asynchronous Consumer=======================================
# class MyAsyncConsumer(AsyncConsumer):
#     # This Handler is called when client initially open a connection and is about to finishing handshake
#
#     async def websocket_connect(self, event):
#         print('Connection Connected', event)
#         await self.send({
#             'type': 'websocket.accept'
#         })
#
#     # This Handler is called When data received from client
#
#     async def websocket_receive(self, event):
#         print('Message Received', event['text'])
#
#         for i in range(50):
#             await self.send(
#                 dict(type='websocket.send', text=str(i))
#             )
#             await asyncio.sleep(1)
#
#     # This Handler is called when client lost the connection closing the connection the server lose the connection
#
#     async def websocket_disconnect(self, event):
#         print('connection disconnected')
#         raise StopConsumer()
#
# # ==========================Generic Web_socket Consumers ===============================================
#
# class WebsocketConsumers(WebsocketConsumer):
#     def connect(self):
#         self.accept()
#
#     def receive(self, text_data=None, bytes_data=None):
#         print(text_data)  # message from client
#         self.send(text_data='saqib')  # message from server to client
#         self.send(bytes_data)  # To send binary frame to client
#         self.close()  # To forcefully reject connection
#         self.close(code=3090)  # Add a custom web_socket Error Code
#
#     def disconnect(self, code):
#         print('web_socket disconnect ', code)
#
#
# class AsyncWebsocketConsumers(AsyncWebsocketConsumer):
#     async def connect(self):
#         await self.accept()
#
#     async def receive(self, text_data=None, bytes_data=None):
#         print(text_data)  # message from client
#         await self.send(text_data='saqib')  # message from server to client
#         await self.send(bytes_data)  # To send binary frame to client
#         await self.close()  # To forcefully reject connection
#         await self.close(code=3090)  # Add a custom web_socket Error Code
#
#     async def disconnect(self, code):
#         print('web_socket disconnect ', code)
from channel.models import Group, Chat


class SyncWebsocketConsumers(WebsocketConsumer):
    def connect(self):
        # get group name from route
        self.group_name = self.scope['url_route']['kwargs']['channel_name']
        # create or get group
        async_to_sync(self.channel_layer.group_add)(self.group_name, self.channel_name)
        self.accept()

    def receive(self, text_data=None, bytes_data=None):
        # message from Client is came in text data
        print("message from client", text_data)
        # convert string into python dict(used form send message)
        data = json.loads(text_data)
        print(data)
        print(data['msg'])
        # send message into
        async_to_sync(self.channel_layer.group_send)(
            self.group_name,
            dict(type='chat.message', message=data['msg'])
        )

    # create handler for type chat.message and in handler is chat_message
    def chat_message(self, event):
        self.send(json.dumps({'msg': event['message']}))

    def disconnect(self, code):
        print('web_socket disconnect ', code)


class AsyncWebsocketConsumers(AsyncWebsocketConsumer):
    async def connect(self):
        # get group name from route
        self.group_name = self.scope['url_route']['kwargs']['channel_name']
        # create or get group
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def receive(self, text_data=None, bytes_data=None):
        # message from Client is came in text data
        print("message from client", text_data)
        # convert string into python dict(used form send message)
        data = json.loads(text_data)
        group = await database_sync_to_async(Group.objects.get)(name=self.group_name)
        if self.scope['user'].is_authenticated:
            chat = Chat(
                group=group,
                text=data['msg']
            )
            await database_sync_to_async(chat.save)()
            print(type(data))
            print(data)
            print(data['msg'])
            # send message into
            await self.channel_layer.group_send(
                self.group_name,
                dict(type='chat.message', message=data['msg'])
            )
        else:
            await self.send(text_data=json.dumps({'msg':'login required'}))
        # create handler for type chat.message and in handler is chat_message

    async def chat_message(self, event):
        print('event is', event)
        await self.send(json.dumps({'msg': event['message']}))


async def disconnect(self, code):
    print('web_socket disconnect ', code)
    print(self.channel_name)
