from django.apps import AppConfig


class SoilTypeConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "agriwise.soil_type"

    def ready(self):
        try:
            import agriwise.soil_type.signals.handlers  # noqa F401
        except ImportError:
            pass
