# from asgiref.sync import async_to_sync 
from channels.generic.websocket import AsyncJsonWebsocketConsumer

class MessageConsumer(AsyncJsonWebsocketConsumer): 
    async def connect(self):
        # Connect a channel named `self.channel_name`
        # to the group `message`
        await self.channel_layer.group_add("message" , self.channel_name)
       
        # Accepts connection
        await self.accept()

    async def disconnect(self, close_code):
        # Disables a channel named `self.channel_name`
        # from the group `message`
        await self.channel_layer.group_discard("message" , self.channel_name)

    async def receive(self, text_data=None, bytes_data=None):

        await self.channel_layer.group_send(
            'message', {
                'type': 'message.sent',
                'content': 'this is a group message'
            })

        await self.send_json({
                'content': 'Hello World!'
            })

    # Method `message_sent` - event handler` message.sent`
    async def message_sent(self, event):
        # Sends a message on the web socket
        await self.send_json({
                'content': event['content']
            })