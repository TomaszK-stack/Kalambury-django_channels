from django.contrib.auth import login , authenticate, logout
from django.shortcuts import render, HttpResponse, redirect
from http.server import BaseHTTPRequestHandler
from .models import Pokoj, Profile
from . import rooms_consumers as rc
from .forms import RegisterForm
from django.contrib.auth.models import User

# Create your views here.
def main_view(request):
    user = request.user
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username = username , password = password)
        print("logowanie trwa")
        if user is not None:
            print("loguje")
            login(request , user)


    return render(request , "main.html", {"user": user})


def rej_view(request):
    form = RegisterForm()
    if request.method == 'POST':
        print("Post")
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password1"]
            print(username)

            user = User(username = form.cleaned_data["username"], password = form.cleaned_data["password1"])
            return redirect("/")

    return render(request, 'rej.html', {'form': form})


def kalambury(request, room_name = None):


    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username = username , password = password)
        print("logowanie trwa")
        if user is not None:
            print("loguje")
            login(request , user)


    if request.user.is_authenticated:

        print(request.user)
        profile = Profile.objects.filter(user=request.user).first()
        user = request.user
        username = user.username

        game_name = "/kalambury/"
        pokoje = rc.pokoje


        if room_name == None:


            return render(request, "index.html", {"game_name":game_name, "pokoje":pokoje})
        else:
            return render(request, "kalambury.html", {"room_name": room_name,  "username":username})

    else:
        return render(request, "unlogged.html")

def user_logout(request):
    logout(request)
    return render(request, "main.html")


def test_room(request, room_name):
    return render(request , 'chatroom.html' , {
        'room_name': room_name
    })

