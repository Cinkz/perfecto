from rest_framework import exceptions, serializers


class RelatedSerializerField(serializers.RelatedField):
    def __init__(self, **kwargs):
        self.lookup_field = kwargs.pop('lookup_field')
        self.serializer = kwargs.pop('serializer')

        super(RelatedSerializerField, self).__init__(**kwargs)

    def use_pk_only_optimization(self):
        return False

    def to_internal_value(self, data):
        if not isinstance(data, dict):
            raise exceptions.ValidationError(code='dictionary_required', detail='Input data should be a dictionary.')

        if not data.has_key(self.lookup_field):
            raise exceptions.ValidationError(code='lookup_field_required', detail='Lookup field: {lookup_field} is required.'.format(lookup_field=self.lookup_field))

        query = {}
        query[self.lookup_field] = data[self.lookup_field]

        if not self.get_queryset().filter(**query).exists():
            raise exceptions.NotFound()

        return self.get_queryset().get(**query)

    def to_representation(self, value):
        return self.serializer(value, context=self.context).data
        