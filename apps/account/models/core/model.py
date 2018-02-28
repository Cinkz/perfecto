from __future__ import unicode_literals

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.postgres.fields import JSONField
from django.db import models

from .manager import UserManager


class User(AbstractBaseUser):
    oauth_id = models.CharField(
        blank=True,
        db_index=True,
        max_length=255,
    )
    username = models.CharField(
        db_index=True,
        max_length=255,
        unique=True,
    )
    email = models.EmailField(
        blank=True,
        db_index=True,
        max_length=255,
    )
    tel = models.CharField(
        blank=True,
        db_index=True,
        max_length=255,
    )
    avatar = models.URLField(
        blank=True,
        max_length=1023,
    )
    first_name = models.CharField(
        blank=True,
        db_index=True,
        max_length=255,
    )
    last_name = models.CharField(
        blank=True,
        db_index=True,
        max_length=255,
    )

    ADMIN = 0
    CLIENT = 1
    MERCHANDISER = 2
    PATTERNMAKER = 3
    ROLES = (
        (ADMIN, 'Admin'),
        (CLIENT, 'Client'),
        (MERCHANDISER, 'Merchandiser'),
        (PATTERNMAKER, 'Patternmaker',)
    )
    role = models.IntegerField(
        choices=ROLES,
    )

    OFFLINE = 0
    FREE = 1
    LEFT = 2
    BUSY = 3
    STATUSES = (
        (OFFLINE, 'Active'),
        (FREE, 'Inactive'),
        (LEFT, 'Left'),
        (BUSY, 'Busy'),
    )
    status = models.IntegerField(
        choices=STATUSES,
        default=OFFLINE,
    )
    is_oauth_enabled = models.BooleanField(
        default=False,
    )

    config = JSONField(
        default=dict,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
    )

    objects = UserManager()

    USERNAME_FIELD = 'username'

    def get_full_name(self):
        if all(ord(c) < 128 for c in self.first_name) and all(ord(c) < 128 for c in self.last_name):
            return '{first_name} {last_name}'.format(
                first_name=self.first_name,
                last_name=self.last_name,
            )
        return '{last_name}{first_name}'.format(
            first_name=self.first_name,
            last_name=self.last_name,
        )

    def get_short_name(self):
        return self.get_full_name()

    def __unicode__(self):
        return self.get_full_name()

    class Meta:
        app_label = 'account'
        ordering = ['created_at']
        