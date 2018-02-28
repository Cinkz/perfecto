#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.management.base import BaseCommand

from account.models.core.model import User
from channel.models.core.model import Channel


CHANNELS = [
    {
        'type': Channel.PUBLIC,
    }
]

USERS = [{'first_name': u'\u68ee', 'last_name': u'\u4e8e', 'tel': u'', 'role': 2, 'password': u'pbkdf2_sha256$30000$p2aOjKo1Alpk$fH8B4zB4J0ZNeQ+hVDDZdoOzQ8hCCTOZ2SK31yF567k=', 'email': u'samyu@dzfaner.com'}, {'first_name': u'R coe', 'last_name': u'', 'tel': u'+8618688468383', 'role': 2, 'password': u'pbkdf2_sha256$30000$ZvGCYGjYk9XM$wJQn2NoPxWFUdMPuYe+MYtS4CeX+WALBReCzFhyvHZE=', 'email': u'289645710@qq.com'}, {'first_name': u'Be', 'last_name': u'Peng', 'tel': u'+8618620637773', 'role': 2, 'password': u'pbkdf2_sha256$30000$lO7KHaxHRvET$dB/+lXFxrkFTvD0vuyx2SpyTPEeFIXNLOwPnvPDj5ro=', 'email': u'122630653@qq.com'}, {'first_name': u'\u5b87\u6674', 'last_name': u'\u5e9e', 'tel': u'+8618813968491', 'role': 2, 'password': u'pbkdf2_sha256$30000$kEdH22PbJoPi$IWVVdhEWtxKFUSo4GALgm0WIHoSAJ/DKCCcn7liS17Q=', 'email': u'470622304@qq.com'}, {'first_name': u'\u96e8\u7af9', 'last_name': u'\u51cc', 'tel': u'+8618898600281', 'role': 2, 'password': u'pbkdf2_sha256$30000$Q9TAWiHFB4XD$yuRHkgB2Xs0HKJeQ6peHVz/fuhgn0dN0ol7OZ45Abmw=', 'email': u'582455637@qq.com'}, {'first_name': u'\u4e50\u5982', 'last_name': u'\u90b1', 'tel': u'+8618813968509', 'role': 2, 'password': u'pbkdf2_sha256$30000$ASMx2omIzsdp$jMJQNJJvJlTiDQcdClS/0jsB3JBd3hiiXJHzPGaNrIQ=', 'email': u'1335171586@qq.com'}, {'first_name': u'\u7d6e\u96ef', 'last_name': u'\u6e29', 'tel': u'+8618813968559', 'role': 2, 'password': u'pbkdf2_sha256$30000$fRDseJJNajwM$4IKtMKnFRdCzkpyqIApfIFP1XDO2CyKc45DiosNBBoI=', 'email': u'112067157@qq.com'}, {'first_name': u'\u534e\u98de', 'last_name': u'\u6768', 'tel': u'+8618813968520', 'role': 2, 'password': u'pbkdf2_sha256$30000$pwnSiyy0WZ08$vX/LbzCusqdYPRWGnDeoQmPLTB5H9t7V7utlQVeC0wQ=', 'email': u'1562582396@qq.com'}, {'first_name': u'\u6653\u6dcb', 'last_name': u'\u5f20', 'tel': u'+8618813968506', 'role': 2, 'password': u'pbkdf2_sha256$30000$jgei7na64EXF$oy6hS2OQbu6kycPLUTm7Wrg3euMcokKxxVz7jkckP34=', 'email': u'1394995849@qq.com'}, {'first_name': u'\u9999\u7389', 'last_name': u'\u674e', 'tel': u'+8613692659003', 'role': 2, 'password': u'pbkdf2_sha256$30000$wSHq0Y86Sebr$4VnFsWH8cYzVfmMgRjdeL9oyCU2qLi2kvItYn7lTD1o=', 'email': u'1209379590@qq.com'}, {'first_name': u'\u7476\u51fd', 'last_name': u'\u674e', 'tel': u'+8618898600413', 'role': 2, 'password': u'pbkdf2_sha256$30000$sD8BDQd4VlB6$OsR3sRPK6XNyg+PiZ8fXeGImMte9KJstVAmUwt9/N1A=', 'email': u'2671614788@qq.com'}, {'first_name': u'\u6c38\u575a', 'last_name': u'\u8d56', 'tel': u'+8613676299601', 'role': 3, 'password': u'pbkdf2_sha256$30000$29QlyHRQhcY0$r2LTqtb35RiLbAGKk1kFsQ3uDKjpntNIDFyhvz8jQBc=', 'email': u'122802042@qq.com'}, {'first_name': u'\u5fb7\u9752', 'last_name': u'\u5218', 'tel': u'+8615920952115', 'role': 3, 'password': u'pbkdf2_sha256$30000$eHTFia0L6fyN$7gqVROoRWQ+djl33OEeZHQi0KG7HdpOimo0x7hNX96o=', 'email': u'1364204838@qq.com'}, {'first_name': u'\u65b0\u8f89', 'last_name': u'\u674e', 'tel': u'+8613678965270', 'role': 3, 'password': u'pbkdf2_sha256$30000$nLgQ7OeTX4IJ$Ms2A+vwkwcpwWDC1XM/bjAquexIEC0aBKpUFvR/rkQw=', 'email': u'904321835@qq.com'}, {'first_name': u'\u660e\u6708', 'last_name': u'\u5411', 'tel': u'+8615919641259', 'role': 3, 'password': u'pbkdf2_sha256$30000$SdF4loU8MgFF$QZ/TjWuS/m+XSaniArQxZZeqhRspD2w+iURcpsjurzQ=', 'email': u'519109648@qq.com'}, {'first_name': u'\u5e73\u8d35', 'last_name': u'\u5218', 'tel': u'+8618659109107', 'role': 3, 'password': u'pbkdf2_sha256$30000$J2NKe1CJW5Sc$kWIDJbVubXnmH9IuSj7qx9ViXKQriYmSskg9kx6st4I=', 'email': u'897839978@qq.com'}, {'first_name': u'\u514b\u98de', 'last_name': u'\u6b27', 'tel': u'+8618820037458', 'role': 3, 'password': u'pbkdf2_sha256$30000$9gRHnEJh6dhn$dx93AA6Db6mmUpjV7HlRoxEvXdZNkb4EQuOEoyCfK3A=', 'email': u''}, {'first_name': u'\u5146\u98de', 'last_name': u'\u6bdb', 'tel': u'+8615889985843', 'role': 3, 'password': u'pbkdf2_sha256$30000$zPKP7D0PDjXw$cDwjSxJsoTY6CIGzjClyJ12oaPuoSXlA059KKEKOKFg=', 'email': u''}, {'first_name': u'\u514b\u7ec3', 'last_name': u'\u9ec4', 'tel': u'+8613510148913', 'role': 3, 'password': u'pbkdf2_sha256$30000$01noJj7vVEuB$ONJ2JVnjrZ3o7pvENrTAioDftENUIEk0F+1N0krDmDk=', 'email': u''}]

class Command(BaseCommand):
    def handle(self, *args, **options):
        for params in CHANNELS:
            if not Channel.objects.filter(**params).exists():
                channel = Channel.objects.create(**params)
                self.stdout.write(self.style.SUCCESS('Created Channel: {id}.'.format(id=channel.id)))
        # for params in USERS:
        #     if not User.objects.filter(email=params['email']).exists():
        #         user = User.objects.create(**params)
        #         self.stdout.write(self.style.SUCCESS('Created User: {full_name}.'.format(full_name=user.get_full_name())))
        for params in USERS:
            password = params.pop('password')
            user = User.objects.create(password='password', **params)
            user.password = password
            user.save()
