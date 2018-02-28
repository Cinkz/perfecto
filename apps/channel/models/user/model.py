from __future__ import unicode_literals

from django.contrib.postgres.fields import JSONField
from django.db import models


class ChannelUser(models.Model):
    channel = models.ForeignKey(
        'Channel',
        related_name='channel_user_set',
    )
    user = models.ForeignKey(
        'account.User',
        related_name='channel_user_set',
    )

    alias = models.CharField(
        max_length=255,
    )
    unread_message_count = models.IntegerField(
        default=0,
    )
    authorization = JSONField(
        default=dict,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
    )

    def __unicode__(self):
        return self.alias

    class Meta:
        app_label = 'channel'
        ordering = ['created_at']
