from __future__ import unicode_literals

from rest_framework import serializers

from account.models.core.model import User
from account.models.core.serializer import UserSerializer
from utility.serializer import DynamicFieldsModelSerializer, RelatedSerializerField

from .model import ChannelUser


class ChannelUserListSerializer(serializers.ListSerializer):
    def create(self, validated_data):
        channel = self.context['channel']

        alias = ''
        for cu in channel.channel_user_set.all():
            if len(cu.alias) > len(alias):
                alias = cu.alias
        for item in validated_data:
            if not 'alias' in item:
                item['alias'] = alias

        channel_users = [ChannelUser(channel=channel, **item) for item in validated_data if not channel.users.filter(id=item['user'].id).exists()]
        return ChannelUser.objects.bulk_create(channel_users)

    def update(self, instances, validated_data):
        channel = self.context['channel']
        instance_mapping = { instance.user.id: instance for instance in instances }
        data_mapping = { item['user'].id: item['user'] for item in validated_data }

        channel_users_to_create = []
        for instance in instances:
            if not data_mapping.has_key(instance.user.id):
                instance.delete()

        channel_users_to_create = [ChannelUser(channel=channel, **item) for item in validated_data if not instance_mapping.has_key(item['user'].id)]
        ChannelUser.objects.bulk_create(channel_users_to_create)
        return ChannelUser.objects.filter(channel=channel)

class ChannelUserSerializer(DynamicFieldsModelSerializer):
    user = RelatedSerializerField(
        lookup_field='id',
        queryset=User.objects.all(),
        serializer=UserSerializer,
    )
    alias = serializers.CharField(
        max_length=255,
        required=False,
    )

    def create(self, validated_data):
        validated_data['channel'] = self.context['channel']
        ret, created = ChannelUser.objects.get_or_create(**validated_data)
        return ret

    class Meta:
        list_serializer_class = ChannelUserListSerializer
        model = ChannelUser
        fields = (
            'id',
            'user',
            'alias',
            'authorization',
            'created_at',
            'updated_at',
        )
        read_only_fields = (
            'id',
            'authorization',
            'created_at',
            'updated_at',
        )
