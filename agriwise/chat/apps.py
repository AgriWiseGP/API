from django.apps import AppConfig


class ChatConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "agriwise.chat"

    def ready(self):
        try:
            import agriwise.chat.signals.handlers  # noqa F401
        except ImportError:
            pass
