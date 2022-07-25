import asyncio
from time import sleep

from channels.consumer import SyncConsumer, AsyncConsumer

# ======================Synchronous Consumer========================================================
from channels.exceptions import StopConsumer


class MyConsumer(SyncConsumer):
    # This Handler is called when client initially open a connection and is about to finishing handshake

    def websocket_connect(self, event):
        print('Connection Connected', event)
        self.send({
            'type': 'websocket.accept'
        })

    # This Handler is called When data received from client

    def websocket_receive(self, event):
        print('Message Received', event['text'])

        for i in range(50):
            self.send(
                dict(type='websocket.send', text=str(i))
            )
            sleep(1)

    # This Handler is called when client lost the connection closing the connection the server lose the connection

    def websocket_disconnect(self, event):
        print('Connection Disconnected', event)
        raise StopConsumer()


# =============================Asynchronous Consumer=======================================
class MyAsyncConsumer(AsyncConsumer):
    # This Handler is called when client initially open a connection and is about to finishing handshake

    async def websocket_connect(self, event):
        print('Connection Connected', event)
        await self.send({
            'type': 'websocket.accept'
        })

    # This Handler is called When data received from client

    async def websocket_receive(self, event):
        print('Message Received', event['text'])

        for i in range(50):
            await self.send(
                dict(type='websocket.send', text=str(i))
            )
            await asyncio.sleep(1)

    # This Handler is called when client lost the connection closing the connection the server lose the connection

    async def websocket_disconnect(self, event):
        print('connection disconnected')
        raise StopConsumer()
