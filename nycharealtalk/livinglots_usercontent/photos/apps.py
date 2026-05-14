from django.apps import AppConfig


class PhotosAppConfig(AppConfig):
    name = 'livinglots_usercontent.photos'

    def ready(self):
        try:
            from actstream import registry
            from . import signals

            registry.register(self.get_model('Photo'))
        except ImportError:
            # django-activity-stream is not installed and that's okay
            pass
