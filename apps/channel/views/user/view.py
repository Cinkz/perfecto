from __future__ import unicode_literals

from rest_framework import viewsets
from rest_framework.decorators import list_route
from rest_framework.response import Response

from channel.models.user.model import ChannelUser
from channel.models.user.serializer import ChannelUserSerializer
from channel.views.core.mixin import ChannelRootMixin, MyChannelRootMixin


class NestedChannelUserViewSet(ChannelRootMixin, viewsets.ModelViewSet):
    queryset = ChannelUser.objects.all()
    serializer_class = ChannelUserSerializer

class MyNestedChannelUserViewSet(MyChannelRootMixin, viewsets.ModelViewSet):
    queryset = ChannelUser.objects.all()
    serializer_class = ChannelUserSerializer

    @list_route(methods=['post'], url_path='bulk-create')
    def bulk_create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @list_route(methods=['patch'], url_path='bulk-update')
    def bulk_update(self, request, *args, **kwargs):
        channel = self.get_channel()
        serializer = self.get_serializer(ChannelUser.objects.filter(channel=channel), data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
