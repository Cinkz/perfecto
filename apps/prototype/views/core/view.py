from __future__ import unicode_literals

from rest_framework import viewsets

from account.views.core.mixin import UserRootMixin
from prototype.models.core.model import Prototype
from prototype.models.core.serializer import PrototypeSerializer


class PrototypeViewSet(viewsets.ModelViewSet):
    queryset = Prototype.objects.all()
    serializer_class = PrototypeSerializer

class MyPrototypeViewSet(PrototypeViewSet):
    def get_queryset(self):
        queryset = super(MyPrototypeViewSet, self).get_queryset()
        return queryset.filter(designed_by=self.request.user)

class NestedPrototypeViewSet(UserRootMixin, viewsets.ModelViewSet):
    queryset = Prototype.objects.all()
    serializer_class = PrototypeSerializer

    def get_queryset(self):
        queryset = super(UserRootMixin, self).get_queryset()
        return queryset.filter(designed_by=self.get_user())
