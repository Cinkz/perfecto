from __future__ import unicode_literals

from django.conf.urls import include, url

from .views.core.router import router as core
from .views.user.router import router as user

urlpatterns = [
    url(r'', include(core.urls)),
    url(r'', include(user.urls)),
]
