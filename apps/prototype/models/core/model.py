from __future__ import unicode_literals

from django.contrib.postgres.fields import JSONField
from django.db import models

from utility.validator import ListValidator


class Prototype(models.Model):
    sid = models.CharField(
        max_length=255,
        unique=True,
    )
    name = models.CharField(
        max_length=255,
    )
    description = models.TextField(
        blank=True,
    )
    designer = JSONField(
        default=dict
    )

    schemes = JSONField(
        default=list,
        validators=[ListValidator(
            code='invalid',
            message='Value should be a list of dictionary.',
        )],
    )
    specsheets = JSONField(
        default=list,
        validators=[ListValidator(
            code='invalid',
            message='Value should be a list of dictionary.',
        )],
    )

    samples = JSONField(
        default=list,
        validators=[ListValidator(
            code='invalid',
            message='Value should be a list of dictionary.',
        )],
    )
    renderings = JSONField(
        default=list,
        validators=[ListValidator(
            code='invalid',
            message='Value should be a list of dictionary.',
        )],
    )
    blueprints = JSONField(
        default=list,
        validators=[ListValidator(
            code='invalid',
            message='Value should be a list of dictionary.',
        )],
    )

    designed_by = models.ForeignKey(
        'account.User',
        related_name='prototypes',
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
    )

    def __unicode__(self):
        return self.name

    class Meta:
        app_label = 'prototype'
        ordering = ['created_at']
