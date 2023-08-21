from django.apps import AppConfig

class AuthenticationConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "authentication"

    def ready(self):
        from .auth_backends import custom_auth
