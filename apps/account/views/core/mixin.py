from __future__ import unicode_literals

from rest_framework import exceptions

from account.models.core.model import User


class UserRootMixin(object):
    def get_user(self):
        query = {'id': self.kwargs['user_id']}
        if not User.objects.filter(**query).exists():
            raise exceptions.NotFound(detail='User not found.')
        return User.objects.get(**query)
