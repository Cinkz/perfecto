from __future__ import unicode_literals

from rest_framework import routers

from .view import ChannelViewSet, MyChannelViewSet


router = routers.DefaultRouter(trailing_slash=False)

router.register(
    r'channels',
    ChannelViewSet,
    base_name='channel',
)
router.register(
    r'my-channels',
    MyChannelViewSet,
    base_name='my-channel',
)
