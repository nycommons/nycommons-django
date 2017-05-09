from django.apps import AppConfig
from django.db.models.signals import post_save


class GroundtruthConfig(AppConfig):
    name = 'groundtruth'
    verbose_name = 'Groundtruth Records'

    def ready(self):
        import django_monitor
        GroundtruthRecord = self.get_model('GroundtruthRecord')
        django_monitor.nq(GroundtruthRecord)

        # Disconnect monitor's post-save handler, moderation will be handled in the
        # view
        from django_monitor.util import save_handler
        post_save.disconnect(save_handler, sender=GroundtruthRecord)

        from . import signals
