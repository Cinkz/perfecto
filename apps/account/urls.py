from __future__ import unicode_literals

from django.conf.urls import include, url

from .views.core.router import router as core

urlpatterns = [
    url(r'', include(core.urls)),
]
