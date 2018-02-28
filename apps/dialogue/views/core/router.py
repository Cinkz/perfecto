from __future__ import unicode_literals

from rest_framework import routers

from .view import NestedDialogueViewSet, MyNestedDialogueViewSet


router = routers.DefaultRouter(trailing_slash=False)

router.register(
    r'channels/(?P<channel_id>[0-9]+)/dialogues',
    NestedDialogueViewSet,
    base_name='channel-dialogue',
)
router.register(
    r'my-channels/(?P<channel_id>[0-9]+)/dialogues',
    MyNestedDialogueViewSet,
    base_name='my-channel-dialogue',
)
