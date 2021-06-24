from business.views import employees
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from asgiref.sync import async_to_sync, sync_to_async
from channels.layers import get_channel_layer
import json

from .models import Room, RoomMessage
from user.models import User
from business.models import Business,Employee

# Handles how users receicve and send messages from and to business
class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.business_id = self.scope['url_route']['kwargs']['business_id']
        self.username = self.scope['url_route']['kwargs']['username']
        self.room_group_name = f'chat_{self.business_id}_{self.username}'
        # Create new room if room does not exist
        await database_sync_to_async(self.create_new_room)()
    
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    # Adds new room to database
    def create_new_room(self):
        try:
            customer = User.objects.get(username = self.username)
            business = Business.objects.get(id = self.business_id)
            Room.objects.create(business=business,customer=customer,room_name=self.room_group_name)
            print("new room created")
        except Exception as e:
            print(e)

    # def delete_room(self):
    #     Room.objects.filter(room_name = self.room_group_name).delete()
    #     return None

    async def disconnect(self,close_code):
        # self.room_db = await database_sync_to_async(self.delete_room)()
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
    # Handles messages received
    async def receive(self,text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        customer_created = text_data_json['customer_created']
        
        # If message by user save 
        if customer_created:
            await database_sync_to_async(self.save_message)(message=message,customer_created=customer_created)

        # Handles how message is sent back to chat room
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chatroom_message',
                'message':message,
                'customer_created':customer_created,
            }
        )

    # Handles how message is sent back to chat room
    async def chatroom_message(self,event):
        message = event['message']
        customer_created = event['customer_created']
        
        # Send message to chat
        await self.send(text_data=json.dumps({
            'message':message,
            'customer_created':customer_created
        }))

    # Save message to database
    def save_message(self,message,customer_created):
        room = Room.objects.get(room_name = self.room_group_name)
        new_message = RoomMessage.objects.create(
            room = room,
            message = message,
            customer_created = customer_created
        )
        new_message.save()

# Handles how businesses send and receive messages to and from customers
class ChatAdminConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.business_id = self.scope['url_route']['kwargs']['business_id']
        self.room_group_name = self.scope['url_route']['kwargs']['room_name']
        self.employee_id = self.scope['url_route']['kwargs']['employee_id']
    
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        await self.accept()

    # async def disconnect(self,close_code):
    #     # self.room_db = await database_sync_to_async(self.delete_room)()
    #     await self.channel_layer.group_discard(
    #         self.room_group_name,
    #         self.channel_name
    #     )
    
    # Handles how messages are received
    async def receive(self,text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        customer_created = text_data_json['customer_created']
        
        # If message is by business save
        if not customer_created:
            await database_sync_to_async(self.save_message)(message=message,customer_created = customer_created)
        
        # Handles how messages are sent back to chatroom
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chatroom_message',
                'message':message,
                'customer_created':customer_created,
            }
        )
    
    # Handles how messages are sent back to chatroom
    async def chatroom_message(self,event):
        message = event['message']
        customer_created = event['customer_created']
        
        await self.send(text_data=json.dumps({
            'message':message,
            'customer_created':customer_created
        }))
    
    # Saves messages to database
    def save_message(self,message,customer_created):
        if self.employee_id == "creator":
            employee = None
        else:
            employee = Employee.objects.get(id = self.employee_id)
        room = Room.objects.get(room_name = self.room_group_name)
        new_message = RoomMessage.objects.create(
            room = room,
            message = message,
            customer_created = customer_created,
            employee = employee
        )
        new_message.save()
