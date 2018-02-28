from __future__ import unicode_literals

from django.db import models


class Channel(models.Model):
    PUBLIC = 0
    ROUTINE = 1
    TASK = 2
    TYPES = (
        (PUBLIC, 'Public'),
        (ROUTINE, 'Routine'),
        (TASK, 'Task'),
    )
    type = models.IntegerField(
        choices=TYPES,
    )
    users = models.ManyToManyField(
        'account.User',
        blank=True,
        related_name='channels',
        through='channel.ChannelUser',
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
    )

    def __init__(self, *args, **kwargs):
        users = kwargs.pop('users', [])
        super(Channel, self).__init__(*args, **kwargs)
        self.env = { 'users': users }

    def __unicode__(self):
        return str(self.id)

    class Meta:
        app_label = 'channel'
        ordering = ['created_at']
