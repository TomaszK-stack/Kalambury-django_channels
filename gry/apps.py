from django.apps import AppConfig


class GryConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'gry'
    def ready(self):
        from . import signals
