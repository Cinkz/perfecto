from __future__ import unicode_literals

from rest_framework import exceptions

from account.models.core.model import User
from account.models.core.serializer import UserSerializer
from utility.serializer import DynamicFieldsModelSerializer

from .model import Dialogue


class DialogueSerializer(DynamicFieldsModelSerializer):
    def create(self, validated_data):
        validated_data['channel'] = self.context['channel']
        validated_data['created_by'] = self.context['request'].user

        if validated_data.get('event', {}).get('type', None) == 'invoice':
            payer_id = validated_data['data'].get('payer', None)
            if not payer_id:
                raise exceptions.ValidationError({ 'payer': ['This field is required.'] })
            if not User.objects.filter(id=payer_id).exists():
                raise exceptions.NotFound(detail='User not found.')
            payer = User.objects.get(id=payer_id)
            validated_data['data']['payer'] = UserSerializer(payer, context=self.context).data
            validated_data['data']['amount'] = sum([item.get('amount', 0) for item in validated_data.get('data', {}).get('items', [])])

        return super(DialogueSerializer, self).create(validated_data)

    class Meta:
        model = Dialogue
        fields = (
            'id',
            'text',
            'data',
            'files',
            'event',
            'author',
            'created_at',
            'updated_at',
        )
        read_only_fields = (
            'id',
            'author',
            'created_at',
            'updated_at',
        )
