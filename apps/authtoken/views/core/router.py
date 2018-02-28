from __future__ import unicode_literals

from rest_framework import routers

from .view import AuthTokenViewSet


router = routers.DefaultRouter(trailing_slash=False)

router.register(
    r'auth',
    AuthTokenViewSet,
    base_name='auth',
)
