#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db.models import F
from django.db.models.signals import post_save
from django.dispatch import receiver

from dialogue.models.core.model import Dialogue


@receiver(post_save, sender=Dialogue, weak=False, dispatch_uid='dialogue:core:supervise:post-save')
def post_save_handler(sender, **kwargs):
    instance = kwargs['instance']
    created = kwargs['created']

    if created:
        instance.channel.channel_user_set.exclude(user=instance.created_by).update(unread_message_count=F('unread_message_count') + 1)
