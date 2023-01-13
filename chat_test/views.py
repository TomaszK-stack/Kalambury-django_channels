from django.shortcuts import render

# Create your views here.
def chat_view(request):
    return render(request, "index.html")


def room(request, room_name):
    return render(request, "room.html", {"room_name": room_name})