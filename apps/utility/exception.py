from __future__ import unicode_literals

from django.core.exceptions import PermissionDenied
from django.http import Http404
from rest_framework import exceptions, status
from rest_framework.compat import set_rollback
from rest_framework.response import Response


def get_full_details(detail):
    if isinstance(detail, list):
        return [get_full_details(item) for item in detail]
    elif isinstance(detail, dict):
        return {key: get_full_details(value) for key, value in detail.items()}
    return {
        'code': detail.code.upper(),
        'description': detail,
    }

def handler(exc, context):
    if isinstance(exc, exceptions.APIException):
        headers = {}
        if getattr(exc, 'auth_header', None):
            headers['WWW-Authenticate'] = exc.auth_header
        if getattr(exc, 'wait', None):
            headers['Retry-After'] = '%d' % exc.wait

        data = get_full_details(exc.detail)

        set_rollback()
        return Response(data, status=exc.status_code, headers=headers)

    elif isinstance(exc, Http404):
        data = {
            'code': 'NOT_FOUND',
            'description': 'Not found.',
        }

        set_rollback()
        return Response(data, status=status.HTTP_404_NOT_FOUND)

    elif isinstance(exc, PermissionDenied):
        print dir(exc)
        data = {
            'code': 'PERMISSION_DENIED',
            'description': 'Permission denied.',
        }

        set_rollback()
        return Response(data, status=status.HTTP_403_FORBIDDEN)

    return None
    