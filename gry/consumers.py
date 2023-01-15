import json
from . import rooms_consumers as rc
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
from .models import Kalambury_slowa
import random

class ChatConsumer(WebsocketConsumer):
    slowo = ""

    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "chat_%s" % self.room_name

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
            if message == self.slowo:
                async_to_sync(self.channel_layer.group_send)(
                    self.room_group_name , {"type": "koniec" })




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
            if x(czy_pozwolic) == True:
                uzytkownicy[self] = True
                rc.rooms_consumers[self.room_name] = uzytkownicy
                numer = random.randint(0, len(rc.slowa))
                self.slowo = rc.slowa[numer]
                async_to_sync(self.send(text_data = json.dumps(
                    {"type": "slowo" , "slowo": slowo})
                ))




    # Receive message from room group
    def chat_message(self, event):
        message = event["message"]
        type = "chat_message"
        # Send message to WebSocket
        self.send(text_data=json.dumps({"message": message, "type":type}))

    def drawing(self, event):
        image = event["image"]
        type = "image_message"
        self.send(text_data = json.dumps({"image":image, "type":type}))

def zapytanie(slownik):
    for key in slownik:
        if slownik[key] == True:
            return False
        else:
            return True