import json
from . import rooms_consumers as rc
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
from .models import Kalambury_slowa
import random

class ChatConsumer(WebsocketConsumer):

    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "chat_%s" % self.room_name
        if self.room_name not in rc.pokoje:
            rc.pokoje.append(self.room_name)


        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        try:
            uzytkownicy = rc.rooms_consumers[self.room_name]
            uzytkownicy[self] = False
            rc.rooms_consumers[self.room_name] = uzytkownicy
        except KeyError:
            rc.rooms_consumers[self.room_name] = {
                self: False ,

            }

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        if(text_data_json.get("type") == "message"):
            message = text_data_json["message"]

            # Send message to room group
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name, {"type": "chat_message", "message": message}
            )
            slowo = rc.slowo_pokoj[self.room_name]
            if message == slowo:
                username = text_data_json['username']
                async_to_sync(self.channel_layer.group_send)(
                    self.room_group_name , {"type": "koniec", "username":username })
                uzytkownicy = rc.rooms_consumers[self.room_name]
                for uzyt in uzytkownicy:
                    uzytkownicy[uzyt] = False
                rc.rooms_consumers[self.room_name] = uzytkownicy





        elif (text_data_json.get("type") == "drawing"):
            image = text_data_json["image"]
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name, {"type": "drawing", "image":image}
            )
        elif (text_data_json.get("type") == "zapytanie"):
            uzytkownicy = rc.rooms_consumers[self.room_name]
            czy_pozwolic = zapytanie(uzytkownicy)
            x = lambda x: "TAK" if x == True else "NIE"
            async_to_sync(self.send(text_data = json.dumps(
                {"type" : "odpowiedz", "odpowiedz": x(czy_pozwolic) })
            ))
            if x(czy_pozwolic) == "TAK":
                uzytkownicy[self] = True
                rc.rooms_consumers[self.room_name] = uzytkownicy
                numer = random.randint(0, len(rc.slowa)-1)
                slowo = rc.slowa[numer]
                rc.slowo_pokoj[self.room_name] = slowo

                async_to_sync(self.send(text_data = json.dumps(
                    {"type": "slowo" , "slowo": slowo})
                ))
                print("Wysłano słowo")
        elif (text_data_json.get("type") == "hello"):
            username = text_data_json['username']
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name , {"type": "hello", "username": username}
            )



    # Receive message from room group
    def chat_message(self, event):
        message = event["message"]
        type = "chat_message"
        # Send message to WebSocket
        self.send(text_data=json.dumps({"message": message, "type":type}))

    def drawing(self, event):
        image = event["image"]
        self.send(text_data = json.dumps({"image":image, "type":"drawing"}))

    def koniec(self , event):
        username = event['username']

        self.send(text_data = json.dumps({"type": "koniec","username":username }))
    def hello(self, event):
        username = event['username']

        self.send(text_data = json.dumps({"type": "hello", "username": username}))

def zapytanie(slownik):
    for key in slownik:
        if slownik[key] == True:
            return False

    return True