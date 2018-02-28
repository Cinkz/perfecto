from __future__ import unicode_literals

from django.conf.urls import url

from .views.core.view import charge_succeed


urlpatterns = [
    url(r'charges/succeed', charge_succeed),
]
