from django.apps import AppConfig


class LocalsportsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Localsports'

    def ready(self):
        import Localsports.signals



