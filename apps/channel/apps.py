from __future__ import unicode_literals

from django.apps import AppConfig


class ChannelConfig(AppConfig):
    name = 'channel'

    def ready(self):
        import channel.signals.core.supervise
        import channel.signals.user.supervise
