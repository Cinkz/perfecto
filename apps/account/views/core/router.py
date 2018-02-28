from __future__ import unicode_literals

from rest_framework import routers

from .view import UserViewSet


router = routers.DefaultRouter(trailing_slash=False)

router.register(
    r'users',
    UserViewSet,
    base_name='user',
)
