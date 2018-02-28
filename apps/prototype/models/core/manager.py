from __future__ import unicode_literals

from django.db import models

from account.models.core.serializer import UserSerializer


class PrototypeManager(models.Manager):
    def _pre_create(self, *args, **kwargs):
        kwargs['designer'] = UserSerializer(kwargs['designed_by']).data
        derivatives = {}
        return args, kwargs, derivatives

    def _post_create(self, instance, **derivatives):
        pass

    def create(self, *args, **kwargs):
        args, kwargs, derivatives = self._pre_create(*args, **kwargs)
        instance = super(PrototypeManager, self).create(*args, **kwargs)
        self._post_create(instance, **derivatives)
        return instance

    def get_or_create(self, *args, **kwargs):
        args, kwargs, derivatives = self._pre_create(*args, **kwargs)
        instance, created = super(PrototypeManager, self).get_or_create(*args, **kwargs)
        self._post_create(instance, **derivatives)
        return instance, created
