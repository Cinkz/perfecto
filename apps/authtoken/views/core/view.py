from __future__ import unicode_literals

from qiniu import Auth

from django.conf import settings
from jwt import encode
from rest_framework import permissions, viewsets
from rest_framework.decorators import api_view, list_route
from rest_framework.response import Response

from account.models.core.model import User
from account.models.core.serializer import UserSerializer
from authtoken.models.core.serializer import AccessTokenSerializer, OauthSerializer
from channel.models.core.model import Channel


access_key = settings.QINIU_ACCESS_KEY
secret_key = settings.QINIU_SECRET_KEY
bucket_name = settings.QINIU_BUCKET_NAME
q = Auth(access_key, secret_key)

@api_view(['POST'])
def qiniu_token(request):
    token = q.upload_token(bucket_name, None, 7200)
    data = {'token': token}
    return Response(data)

class AuthPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.action in ['login', 'oauth', 'register']:
            return True
        return request.user is not None

class AuthTokenViewSet(viewsets.ViewSet):
    permission_classes = [AuthPermission]

    def get_serializer_context(self):
        return {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self
        }

    @list_route(methods=['post'])
    def register(self, request, *args, **kwargs):
        context = self.get_serializer_context()
        serializer = UserSerializer(data=request.data, context=context)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @list_route(methods=['post'])
    def setting(self, request, *args, **kwargs):
        context = self.get_serializer_context()
        serializer = UserSerializer(request.user, data=request.data, context=context)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @list_route(methods=['post'])
    def login(self, request, *args, **kwargs):
        context = self.get_serializer_context()
        serializer = AccessTokenSerializer(data=request.data, context=context)
        serializer.is_valid(raise_exception=True)
        response = serializer.save()
        return Response(response)

    @list_route(methods=['post'])
    def oauth(self, request, *args, **kwargs):
        context = self.get_serializer_context()
        serializer = OauthSerializer(data=request.data, context=context)
        serializer.is_valid(raise_exception=True)
        response = serializer.save()
        return Response(response)

    @list_route(methods=['get'])
    def inspect(self, request, *args, **kwargs):
        token = request.auth
        access_token = encode(token, settings.PRIVATE_KEYS['auth'], algorithm='RS256')
        if request.user.role == User.CLIENT:
            landing = { 'id': request.user.channels.filter(type=Channel.ROUTINE).first().id }
        else:
            landing = { 'id': request.user.channels.filter(type=Channel.PUBLIC).first().id }

        return Response({
            'access_token': access_token,
            'expires_at': token['expires_at'],
            'landing': landing,
            'user': UserSerializer(request.user, context=self.get_serializer_context()).data,
        })
