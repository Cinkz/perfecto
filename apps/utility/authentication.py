from __future__ import unicode_literals

from django.conf import settings
from django.contrib.auth import get_user_model
from jwt import DecodeError, decode
from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication, get_authorization_header

User = get_user_model()

class TokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth = get_authorization_header(request).split()

        if not auth or auth[0].lower() != 'bearer':
            return None

        if len(auth) == 1:
            raise exceptions.AuthenticationFailed(code='invalid', detail='Invalid token header. No credentials provided.')
        elif len(auth) > 2:
            raise exceptions.AuthenticationFailed(code='invalid', detail='Invalid token header. Token string should not contain spaces.')

        try:
            access_token = auth[1].decode()
        except UnicodeError:
            raise exceptions.AuthenticationFailed(code='invalid', detail='Invalid token header. Token string should not contain invalid characters.')

        return self.authenticate_credentials(access_token)

    def authenticate_credentials(self, access_token):
        try:
            token = decode(access_token, settings.PUBLIC_KEYS['auth'], algorithms='RS256')
        except DecodeError:
            raise exceptions.AuthenticationFailed(code='invalid_token', detail='Invalid token.')

        user = User.objects.get(id=token['user']['id'])
        return (user, token)

    def authenticate_header(self, request):
        return 'Bearer'
