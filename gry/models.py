from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Kalambury_slowa(models.Model):
    slowo = models.TextField()


class Profile(models.Model):
    user = models.OneToOneField(User , on_delete = models.CASCADE , related_name = 'to_user')
    czy_moze_rysowac = models.BooleanField(default = False)
