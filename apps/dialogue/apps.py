from __future__ import unicode_literals

from django.apps import AppConfig


class DialogueConfig(AppConfig):
    name = 'dialogue'

    def ready(self):
        import dialogue.signals.core.supervise
