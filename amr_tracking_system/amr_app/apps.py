from django.apps import AppConfig


class amr_appConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'amr_app'

    def ready(self):
        import amr_app.signals  # Adjust the import path according to your app name

