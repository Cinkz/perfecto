from __future__ import unicode_literals

from django.db.models.signals import post_save
from django.dispatch import receiver

from channel.models.core.model import Channel
from channel.models.user.serializer import ChannelUserSerializer



@receiver(post_save, sender=Channel, weak=False, dispatch_uid='channel:core:supervise:post-save')
def post_save_handler(sender, **kwargs):
    instance = kwargs['instance']
    created = kwargs['created']

    users = instance.env.pop('users', [])
    serializer = ChannelUserSerializer(data=users, many=True, context={ 'channel': instance })
    serializer.is_valid(raise_exception=True)
    serializer.save()
