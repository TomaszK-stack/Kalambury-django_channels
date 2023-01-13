from django.contrib.auth import login , authenticate, logout
from django.shortcuts import render
from http.server import BaseHTTPRequestHandler

# Create your views here.
def main_view(request):
    user = request.user
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username = username , password = password)
        if user is not None:
            login(request , user)


    return render(request , "main.html", {"user": user})

def rej_view(request):


    return render(request, "rej.html")


def kalambury(request, room_name = None):
    game_name = "/kalambury/"

    if room_name == None:
        return render(request, "index.html", {"game_name":game_name})
    else:
        return render(request, "kalambury.html", {"room_name": room_name})

def user_logout(request):
    logout(request)
    return render(request, "main.html")


def test_room(request, room_name):
    return render(request , 'chatroom.html' , {
        'room_name': room_name
    })

