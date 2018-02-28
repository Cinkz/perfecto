from __future__ import unicode_literals

from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256
import base64
import os

from django.conf import settings
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from transaction.models.core.model import Transaction


def decode_base64(data):
    remainder = len(data) % 4
    if remainder:
        data += '=' * (4 - remainder)
    return base64.decodestring(data.encode('utf-8'))

def verify(data, sig):
    signs = decode_base64(sig)
    data = data.decode('utf-8') if hasattr(data, "decode") else data
    pubkeystr = open(os.path.join(settings.DJANGO_ROOT, 'certificates', 'public', 'pingpp.pem')).read()
    pubkey = RSA.importKey(pubkeystr)
    digest = SHA256.new(data.encode('utf-8'))
    pkcs = PKCS1_v1_5.new(pubkey)
    return pkcs.verify(digest, signs)

@api_view(['POST'])
@permission_classes([AllowAny])
def charge_succeed(request):
    if not verify(request.body, request.META.get('HTTP_X_PINGPLUSPLUS_SIGNATURE', '')):
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    if request.data['type'] == 'charge.succeeded':
        try:
            transaction_id = int(request.data['data']['object']['order_no'])
            transaction = Transaction.objects.get(id=transaction_id)
            dialogue = transaction.dialogue
            dialogue.data['paid_at'] = request.data['data']['object']['time_paid']
            dialogue.save()
            return Response(status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
