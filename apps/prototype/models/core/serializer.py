from __future__ import unicode_literals

from account.models.core.model import User
from account.models.core.serializer import UserSerializer
from utility.serializer import DynamicFieldsModelSerializer, RelatedSerializerField

from .model import Prototype


class PrototypeSerializer(DynamicFieldsModelSerializer):
    designed_by = RelatedSerializerField(
        lookup_field='id',
        queryset=User.objects.all(),
        serializer=UserSerializer,
        write_only=True,
    )

    class Meta:
        model = Prototype
        fields = (
            'designed_by',
            'id',
            'sid',
            'name',
            'description',
            'designer',
            'schemes',
            'specsheets',
            'samples',
            'renderings',
            'blueprints',
            'created_at',
            'updated_at',
        )
        read_only_fields = (
            'id',
            'designer',
            'created_at',
            'updated_at',
        )
