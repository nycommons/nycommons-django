from django.apps import AppConfig
from django.db.models.signals import post_save


class StewardConfig(AppConfig):
    name = 'steward'

    def ready(self):
        import django_monitor
        StewardNotification = self.get_model('StewardNotification')
        django_monitor.nq(StewardNotification)

        # Disconnect monitor's post-save handler, moderation will be handled in the
        # view
        from django_monitor.util import save_handler
        post_save.disconnect(save_handler, sender=StewardNotification)

        from . import signals
