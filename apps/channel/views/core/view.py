from __future__ import unicode_literals

from django.db.models import Prefetch
from rest_framework import viewsets

from channel.models.core.model import Channel
from channel.models.core.serializer import ChannelSerializer
from channel.models.user.model import ChannelUser


class ChannelViewSet(viewsets.ModelViewSet):
    queryset = Channel.objects.all()
    serializer_class = ChannelSerializer

class MyChannelViewSet(viewsets.ModelViewSet):
    serializer_class = ChannelSerializer

    def get_queryset(self):
        return self.request.user.channels.prefetch_related(Prefetch('channel_user_set', queryset=ChannelUser.objects.filter(user=self.request.user)))
