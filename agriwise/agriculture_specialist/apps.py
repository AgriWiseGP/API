from django.apps import AppConfig


class AgricultureSpecialistConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "agriwise.agriculture_specialist"

    def ready(self):
        try:
            import agriwise.agriculture_specialist.signals.handlers  # noqa F401
        except ImportError:
            pass
