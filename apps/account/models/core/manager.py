#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os

from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, password, username=None, *args, **kwargs):
        if username is None:
            username = 'perfecto#{code}'.format(code=os.urandom(10).encode('hex'))
        kwargs['username'] = username

        user = self.model(**kwargs)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, username, password):
        user = self.create_user(username=username, password=password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

    def create(self, password, username=None, *args, **kwargs):
        return self.create_user(password=password, username=None, *args, **kwargs)
