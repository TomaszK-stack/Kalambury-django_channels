
from django.contrib import admin
from django.urls import path
from .views import *


urlpatterns = [
    path('', main_view ),
    path('logout', user_logout ),
    path('rej', rej_view ),
    path('kalambury', kalambury ),
    path('kalambury/<str:room_name>/', kalambury ),

]