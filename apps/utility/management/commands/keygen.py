from __future__ import unicode_literals

from os.path import join

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

from django.conf import settings
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            '--filename',
            action='store',
            dest='filename',
            help='Filename to store the key-pairs.',
        )

    def handle(self, *args, **options):
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend(),
        )
        with open(join(settings.DJANGO_ROOT, 'certificates', 'private', options['filename']), 'wb') as keyfile:
            keyfile.write(private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption()
            ))
        public_key = private_key.public_key()
        with open(join(settings.DJANGO_ROOT, 'certificates', 'public', options['filename']), 'wb') as keyfile:
            keyfile.write(public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo,
            ))
