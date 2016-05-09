from django.apps import AppConfig


class LotsAppConfig(AppConfig):
    name = 'lots'

    def ready(self):
        from actstream import registry
        registry.register(self.get_model('Lot'))
