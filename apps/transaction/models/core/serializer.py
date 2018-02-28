from __future__ import unicode_literals

from utility.serializer import DynamicFieldsModelSerializer

from .model import Transaction


class TransactionSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Transaction
        fields = (
            'id',
            'charge',
            'created_at',
            'updated_at',
        )
        read_only_fields = (
            'id',
            'charge',
            'created_at',
            'updated_at',
        )
