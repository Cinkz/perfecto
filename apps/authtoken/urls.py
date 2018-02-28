from __future__ import unicode_literals

from django.conf.urls import include, url

from .views.core.view import qiniu_token
from .views.core.router import router as core


urlpatterns = [
    url(r'qiniu_token', qiniu_token),
    url(r'', include(core.urls)),
]
