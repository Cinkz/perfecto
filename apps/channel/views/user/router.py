from __future__ import unicode_literals

from rest_framework import routers

from .view import NestedChannelUserViewSet, MyNestedChannelUserViewSet


router = routers.DefaultRouter(trailing_slash=False)

router.register(
    r'channels/(?P<channel_id>[0-9]+)/users',
    NestedChannelUserViewSet,
    base_name='channel-user',
)
router.register(
    r'my-channels/(?P<channel_id>[0-9]+)/users',
    MyNestedChannelUserViewSet,
    base_name='my-channel-user',
)
