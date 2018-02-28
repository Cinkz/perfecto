from __future__ import unicode_literals

from rest_framework import routers

from .view import PrototypeViewSet, MyPrototypeViewSet, NestedPrototypeViewSet


router = routers.DefaultRouter(trailing_slash=False)

router.register(
    r'prototypes',
    PrototypeViewSet,
    base_name='prototype',
)
router.register(
    r'my-prototypes',
    MyPrototypeViewSet,
    base_name='my-prototype',
)

router.register(
    r'users/(?P<user_id>[0-9]+)/prototypes',
    NestedPrototypeViewSet,
    base_name='user-prototype',
)
