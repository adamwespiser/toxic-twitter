from django.apps import AppConfig

class ToxicityanalyzerConfig(AppConfig):
    name = 'toxicityanalyzer'

    def ready(self):
        # This is where the startup code goes.
        pass
