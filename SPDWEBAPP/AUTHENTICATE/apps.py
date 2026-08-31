from django.apps import AppConfig


class AuthenticateConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'AUTHENTICATE'

    def ready(self):
        from .signals import connect_signals
        connect_signals()
