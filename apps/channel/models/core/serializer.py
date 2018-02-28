from __future__ import unicode_literals

from rest_framework import serializers

from utility.serializer import DynamicFieldsModelSerializer

from channel.models.user.model import ChannelUser
from .model import Channel


class ChannelRelationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChannelUser
        fields = (
            'alias',
            'unread_message_count',
            'authorization',
            'created_at',
            'updated_at',
        )
        read_only_fields = (
            'alias',
            'unread_message_count',
            'authorization',
            'created_at',
            'updated_at',
        )

class ChannelSerializer(DynamicFieldsModelSerializer):
    relation = serializers.SerializerMethodField(
        read_only=True,
    )

    def __init__(self, *args, **kwargs):
        super(ChannelSerializer, self).__init__(*args, **kwargs)

        print dir(self)
        print self.fields

    def get_relation(self, obj):
        channel_user = obj.channel_user_set.get(user=self.context['request'].user)
        serializer = ChannelRelationSerializer(channel_user)
        return serializer.data

    class Meta:
        model = Channel
        fields = (
            'id',
            'type',
            'relation',
            'created_at',
            'updated_at',
        )
        read_only_fields = (
            'id',
            'relation',
            'created_at',
            'updated_at',
        )
