from django.dispatch import receiver
from .models import *
from django.contrib.auth.models import User
from django.db.models.signals import post_save

@receiver(post_save, sender = User)
def profile_after_user_create(sender, instance, created, *args, **kwargs):
    if created:
        profile = Profile(user = instance)
        profile.save()