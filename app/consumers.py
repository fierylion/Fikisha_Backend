import json
from channels.generic.websocket import AsyncWebsocketConsumer
import asyncio
from .serializers import OrderDeliveryModalSerializer
from .models import OrderDeliveryModal
from asgiref.sync import sync_to_async

class UserOrderConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name=self.scope['url_route']['kwargs']['user_id']
        print(self.room_name)
        self.room_group_name=f'user_{self.room_name}'
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
    async def update_user_orders(self, event):
        data = event['data']
        await self.send(text_data=json.dumps(
            {
                'type':data
            }
        ))

class LocationConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.location_buffer = []
    
       
    
    async def connect(self):
        asyncio.create_task(self.periodic_location_update())
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f"location_{self.room_name}"

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
       
        data = json.loads(text_data)
        # {'latitude': -6.7714211, 'longitude': 39.2399721, 'heading': 0, 'longitudeDelta': 0.003, 'latitudeDelta': 0.003}
    
        # Broadcast location update to room group
        self.location_buffer.append(data)
        print(self.location_buffer)
      
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'location_update',
                'location':data
            }
        )

    async def location_update(self, event):
        location = event["location"]
        # Send location update to client
      
        await self.send(text_data=json.dumps({
            'driver_location': location
        }))
    async def periodic_location_update(self):
    
        while True:
            
            if self.location_buffer and len(self.location_buffer)>0:
                
                last_location = self.location_buffer[-1]
                await self.update_location_in_database_sync(last_location)
                print('done')
                self.location_buffer=[]
       
            await asyncio.sleep(45)
        
    @sync_to_async
    def update_location_in_database_sync(self, location):
        OrderDeliveryModal.objects.filter(agent_id=self.room_name).update(location=json.dumps(location))
      
      


                
class OrderConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = 'drivers_group'
        print(self.room_name)
        self.room_group_name = f"{self.room_name}"

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        print("connected")
        await self.accept()
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
    async def send_order(self,event):
        data = event['data']
        
        await self.send(text_data=json.dumps(data))




   

