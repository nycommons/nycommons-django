from django.apps import AppConfig


class NotesAppConfig(AppConfig):
    name = 'livinglots_usercontent.notes'

    def ready(self):
        try:
            from actstream import registry
            from . import signals

            registry.register(self.get_model('Note'))
        except ImportError:
            # django-activity-stream is not installed and that's okay
            pass
