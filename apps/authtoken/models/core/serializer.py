from __future__ import unicode_literals

from datetime import timedelta

import os, requests

from django.conf import settings
from django.utils import timezone
from jwt import encode
from rest_framework import exceptions, serializers

from account.models.core.model import User
from account.models.core.serializer import UserSerializer
from channel.models.core.model import Channel

class AccessTokenSerializer(serializers.Serializer):
    identifier = serializers.CharField(
        max_length=255,
        write_only=True,
    )
    password = serializers.CharField(
        max_length=255,
        write_only=True,
    )

    def validate_identifier(self, data):
        data = data.strip()
        if len(data) == 0:
            raise exceptions.ValidationError(code='invalid', detail='Identifier cannot be empty value.')

        user = None
        if User.objects.filter(username=data).exists():
            user = User.objects.get(username=data)
        if User.objects.filter(email=data).exists():
            user = User.objects.get(email=data)
        if User.objects.filter(tel=data).exists():
            user = User.objects.get(tel=data)
        if user is None:
            raise exceptions.ValidationError(code='invalid', detail='User account does not exist.')
        return user

    def validate(self, data):
        user = data.pop('identifier')
        password = data.pop('password')
        if not user.check_password(password):
            raise exceptions.AuthenticationFailed(code='invalid', detail='Password does not match the user account.')

        data['user'] = user
        return data

    def create(self, validated_data):
        token = {
            'expires_at': (timezone.now() + timedelta(minutes=30)).isoformat().replace('+00:00', 'Z'),
            'ipv4': self.context['request'].ipv4,
            'user': {
                'id': validated_data['user'].id,
                'role': validated_data['user'].role,
            }
        }
        access_token = encode(token, settings.PRIVATE_KEYS['auth'], algorithm='RS256')
        if validated_data['user'].role == User.CLIENT:
            landing = { 'id': validated_data['user'].channels.filter(type=Channel.ROUTINE).first().id }
        else:
            landing = { 'id': validated_data['user'].channels.filter(type=Channel.PUBLIC).first().id }

        return {
            'access_token': access_token,
            'expires_at': token['expires_at'],
            'landing': landing,
            'user': UserSerializer(validated_data['user']).data,
        }

    def update(self, instance, validated_data):
        raise exceptions.MethodNotAllowed(method=self.context['request'].method)

    class Meta:
        fields = (
            'identifier',
            'password',
        )

class OauthSerializer(serializers.Serializer):
    ticket = serializers.CharField(
        max_length=255,
        write_only=True,
    )

    def create(self, validated_data):
        res = requests.get('http://{domain}/account/getTokenByTicket'.format(domain=settings.OAUTH_API_DOMAIN), params={'ticket': validated_data['ticket']})
        if not res.ok:
            raise exceptions.AuthenticationFailed(detail='Oauth server cannot recognize the ticket.')
        oauth_access_token = res.json().get('data', None)
        if oauth_access_token is None:
            raise exceptions.AuthenticationFailed(detail='Oauth server response is invalid.')
        res = requests.get('http://{domain}/account/getUserInfoByToken'.format(domain=settings.OAUTH_API_DOMAIN), params={'token': oauth_access_token})
        if not res.ok:
            raise exceptions.AuthenticationFailed(detail='Oauth server cannot recognize the token.')
        oauth_user_data = res.json().get('data', {})
        try:
            oauth_user_id = str(oauth_user_data.get('userId'))
        except:
            raise exceptions.AuthenticationFailed(detail='Oauth server respond with invalid user id.')
        params = { 'oauth_id': oauth_user_id }
        user_count = User.objects.filter(**params).count()
        if user_count == 1:
            user = User.objects.get(**params)
        elif user_count == 0:
            params['is_oauth_enabled'] = True
            params['password'] = os.urandom(20).encode('hex')
            params['role'] = User.CLIENT
            avatar = oauth_user_data.get('avatarUrl', None)
            if isinstance(avatar, (str, unicode)):
                params['avatar'] = avatar
            email = oauth_user_data.get('email', None)
            if isinstance(avatar, (str, unicode)):
                params['email'] = email
            tel = oauth_user_data.get('mobile', None)
            if isinstance(tel, (str, unicode)):
                params['tel'] = tel
            realname = oauth_user_data.get('realName', None)
            nickname = oauth_user_data.get('nickName', None)
            if realname is not None and len(realname) > 0:
                params['first_name'] = realname
            elif nickname is not None and len(nickname) > 0:
                params['first_name'] = nickname
            else:
                params['first_name'] = tel[-4:]
            user = User.objects.create(**params)
        else:
            raise exceptions.AuthenticationFailed(detail='Duplicate oauth user_id found in database.')
        token = {
            'expires_at': (timezone.now() + timedelta(minutes=30)).isoformat().replace('+00:00', 'Z'),
            'ipv4': self.context['request'].ipv4,
            'user': {
                'id': user.id,
                'role': user.role,
            }
        }
        access_token = encode(token, settings.PRIVATE_KEYS['auth'], algorithm='RS256')
        if user.role == User.CLIENT:
            landing = { 'id': user.channels.filter(type=Channel.ROUTINE).first().id }
        else:
            landing = { 'id': user.channels.filter(type=Channel.PUBLIC).first().id }

        return {
            'access_token': access_token,
            'expires_at': token['expires_at'],
            'landing': landing,
            'user': UserSerializer(user).data,
        }

    def update(self, instance, validated_data):
        raise exceptions.MethodNotAllowed(method=self.context['request'].method)

    class Meta:
        fields = (
            'ticket',
        )
