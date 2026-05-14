from django.apps import AppConfig


class FilesAppConfig(AppConfig):
    name = 'livinglots_usercontent.files'

    def ready(self):
        try:
            from actstream import registry
            from . import signals

            registry.register(self.get_model('File'))
        except ImportError:
            # django-activity-stream is not installed and that's okay
            pass
