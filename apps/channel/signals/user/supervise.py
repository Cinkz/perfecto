from __future__ import unicode_literals

from django.db.models.signals import pre_save
from django.dispatch import receiver
from rest_framework import exceptions

from channel.models.user.model import ChannelUser


@receiver(pre_save, sender=ChannelUser, weak=False, dispatch_uid='channel:channel-user-set:supervise:pre-save')
def pre_save_handler(sender, **kwargs):
    instance = kwargs['instance']
    if instance.id is None and instance.channel.channel_user_set.filter(user=instance.user).exists():
        raise exceptions.PermissionDenied(code='duplicate', detail='Duplicate user found in the channel.')
