from __future__ import unicode_literals

from django.contrib.postgres.fields import JSONField
from django.db import models

from account.models.core.serializer import UserSerializer
from utility.validator import ListValidator


class Dialogue(models.Model):
    text = models.TextField(
        blank=True,
    )
    data = JSONField(
        default=dict,
    )
    event = JSONField(
        default=dict,
    )
    files = JSONField(
        default=list,
        validators=[ListValidator(
            code='invalid',
            message='Value should be a list of dictionary.',
        )],
    )

    author = JSONField(
        default=dict
    )

    # {
    #     'type': ['text', 'file', 'channel', 'task', 'milestone', 'invoice'],
    #     'file_type': ['image', 'file', 'scheme', 'specsheet', 'sample', 'rendering', 'blueprint'],
    #     'task_type': ['patterning', 'manufacturing'],
    #     'action': ['create'],
    #     'channel': { 'id': 1, 'name': 'XXX'}
    # }

    channel = models.ForeignKey(
        'channel.Channel',
        related_name='dialogues',
    )
    created_by = models.ForeignKey(
        'account.User',
        related_name='dialogues',
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
    )

    def __init__(self, *args, **kwargs):
        super(Dialogue, self).__init__(*args, **kwargs)
        if not self.author:
            self.author = UserSerializer(self.created_by).data

    def __unicode__(self):
        return self.text

    class Meta:
        app_label = 'dialogue'
        ordering = ['created_at']
