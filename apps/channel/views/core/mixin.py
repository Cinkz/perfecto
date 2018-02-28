from __future__ import unicode_literals

from rest_framework import exceptions

from channel.models.core.model import Channel


class ChannelRootMixin(object):
    def get_channel(self):
        query = {'id': self.kwargs['channel_id']}
        if not Channel.objects.filter(**query).exists():
            raise exceptions.NotFound(detail='Channel not found.')
        return Channel.objects.get(**query)

    def get_serializer_context(self):
        context = super(ChannelRootMixin, self).get_serializer_context()
        context['channel'] = self.get_channel()
        return context

    def get_queryset(self):
        queryset = super(ChannelRootMixin, self).get_queryset()
        return queryset.filter(channel=self.get_channel())

class MyChannelRootMixin(ChannelRootMixin):
    def get_channel(self):
        query = {'id': self.kwargs['channel_id']}
        if not self.request.user.channels.filter(**query).exists():
            raise exceptions.NotFound(detail='Channel not found.')
        return self.request.user.channels.get(**query)
