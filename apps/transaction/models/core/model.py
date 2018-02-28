# #!/usr/bin/env python
# # -*- coding: utf-8 -*-
from __future__ import unicode_literals

from os.path import join

import pingpp

from django.conf import settings
from django.contrib.postgres.fields import JSONField
from django.db import models


pingpp.api_key = settings.PINGPP_API_KEY
pingpp.private_key_path = join(settings.DJANGO_ROOT, 'certificates', 'private', 'pingpp-server.pem')

class Transaction(models.Model):
    charge = JSONField(
        default=dict
    )

    dialogue = models.ForeignKey(
        'dialogue.Dialogue',
        related_name='transactions',
    )
    channel = models.CharField(
        max_length=255,
    )
    amount = models.IntegerField()
    ipv4 = models.GenericIPAddressField(
        protocol='IPv4',
    )
    paid = models.BooleanField(
        default=False,
    )
    paid_at = models.DateTimeField(
        blank=True,
        null=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
    )

    def get_order_no(self):
        return '{id:020}'.format(id=self.id)

    def get_charge_object(self, save=True):
        if not self.charge:
            order_no = self.get_order_no()
            if self.channel == 'wx_pub_qr':
                self.charge = pingpp.Charge.create(
                    order_no=order_no,
                    amount=self.amount,
                    app=dict(id=settings.PINGPP_APP_ID),
                    channel=self.channel,
                    currency='cny',
                    client_ip=self.ipv4,
                    subject='服务费',
                    body='点图承衣平台服务费。',
                    extra=dict(product_id=order_no),
                )
            elif self.channel == 'alipay_qr':
                self.charge = pingpp.Charge.create(
                    order_no=order_no,
                    amount=self.amount,
                    app=dict(id=settings.PINGPP_APP_ID),
                    channel=self.channel,
                    currency='cny',
                    client_ip=self.ipv4,
                    subject='服务费',
                    body='点图承衣平台服务费。',
                )
        self.dialogue.data['channel'] = self.charge['channel']
        self.dialogue.data['qrcode'] = self.charge['credential'][self.charge['channel']]
        self.dialogue.data['time_expire'] = self.charge['time_expire']
        self.dialogue.save()
        if save:
            self.save()

    def __unicode__(self):
        return self.get_order_no()

    class Meta:
        app_label = 'transaction'
        ordering = ['created_at']
