from django.apps import AppConfig


class InitConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'init'

    def ready(self):
        import init.signals