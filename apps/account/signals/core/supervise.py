#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from random import choice

from django.db.models.signals import post_save
from django.dispatch import receiver

from account.models.core.model import User
from channel.models.core.model import Channel
from channel.models.user.model import ChannelUser


@receiver(post_save, sender=User, weak=False, dispatch_uid='account:core:supervise:post-save')
def post_save_handler(sender, **kwargs):
    instance = kwargs['instance']
    created = kwargs['created']

    if created:
        if instance.role == User.CLIENT:
            merchandiser = choice(User.objects.filter(role=User.MERCHANDISER))
            channel = Channel.objects.create(type=Channel.ROUTINE, users=[
                { 'user': { 'id': instance.id }, 'alias': '事务频道' },
                { 'user': { 'id': merchandiser.id }, 'alias': '{client_full_name}的事务频道'.format(client_full_name=instance.get_full_name()) }
            ])
            instance.config.update({ 'landing': channel.id })
            instance.save()
        elif instance.role in [User.MERCHANDISER, User.PATTERNMAKER]:
            channel = Channel.objects.get(type=Channel.PUBLIC)
            ChannelUser.objects.create(channel=channel, user=instance, alias='公共频道')
            instance.config.update({ 'landing': channel.id })
            instance.save()
