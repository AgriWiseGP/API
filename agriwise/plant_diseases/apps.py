from django.apps import AppConfig


class PlantDiseasesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "agriwise.plant_diseases"

    def ready(self):
        try:
            import agriwise.plant_diseases.signals.handlers  # noqa F401
        except ImportError:
            pass
