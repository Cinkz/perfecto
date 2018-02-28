from __future__ import unicode_literals

import django_filters

from rest_framework import permissions, viewsets

from account.models.core.model import User
from account.models.core.serializer import UserSerializer


class UserPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.action == 'create':
            return True
        return request.user is not None

    def has_object_permission(self, request, view, obj):
        if view.action in ['update', 'partial_update', 'delete']:
            return obj == request.user
        return True

class UserFilter(django_filters.rest_framework.FilterSet):
    class Meta:
        model = User
        fields = ['role']

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    filter_class = UserFilter
    permission_classes = [UserPermission]
    queryset = User.objects.all()
    serializer_class = UserSerializer
