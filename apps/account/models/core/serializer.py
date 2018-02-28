from __future__ import unicode_literals

from rest_framework import exceptions, serializers, validators

from utility.serializer import DynamicFieldsModelSerializer

from .model import User


class UserSerializer(DynamicFieldsModelSerializer):
    password = serializers.CharField(
        max_length=255,
        required=False,
        write_only=True,
    )
    current_password = serializers.CharField(
        max_length=255,
        required=False,
        write_only=True,
    )
    password_confirmation = serializers.CharField(
        max_length=255,
        required=False,
        write_only=True,
    )

    username = serializers.CharField(
        required=False,
        validators=[validators.UniqueValidator(queryset=User.objects.all())],
    )
    email = serializers.EmailField(
        required=False,
        validators=[validators.UniqueValidator(queryset=User.objects.all())],
    )
    tel = serializers.CharField(
        required=False,
        validators=[validators.UniqueValidator(queryset=User.objects.all())],
    )

    full_name = serializers.CharField(
        read_only=True,
        source='get_full_name',
    )

    def create(self, validated_data):
        errors = {}
        password = validated_data.get('password')
        password_confirmation = validated_data.pop('password_confirmation', None)
        current_password = validated_data.pop('password', None)
        if not password:
            exc = exceptions.ValidationError(code='required', detail='This field is required.')
            errors.setdefault('password', []).extend(exc.detail)
        if not password_confirmation:
            exc = exceptions.ValidationError(code='required', detail='This field is required.')
            errors.setdefault('password', []).extend(exc.detail)
        if password != password_confirmation:
            exc = exceptions.ValidationError(code='invalid', detail='Password confirmation does not match with the password.')
            errors.setdefault('password_confirmation', []).extend(exc.detail)
        if errors:
            raise exceptions.ValidationError(detail=errors)

        validated_data['password'] = password
        validated_data['role'] = User.CLIENT

        return super(UserSerializer, self).create(validated_data)

    def update(self, instance, validated_data):
        current_password = validated_data.pop('current_password', None)
        if current_password:
            errors = {}
            if not instance.check_password(current_password):
                raise exceptions.AuthenticationFailed(detail='Wrong password.')

            password = validated_data.pop('password', None)
            password_confirmation = validated_data.pop('password_confirmation', None)
            if not password:
                exc = exceptions.ValidationError(code='required', detail='This field is required.')
                errors.setdefault('password', []).extend(exc.detail)
            if not password_confirmation:
                exc = exceptions.ValidationError(code='required', detail='This field is required.')
                errors.setdefault('password', []).extend(exc.detail)
            if password != password_confirmation:
                exc = exceptions.ValidationError(code='invalid', detail='Password confirmation does not match with the password.')
                errors.setdefault('password_confirmation', []).extend(exc.detail)
            if errors:
                raise exceptions.ValidationError(detail=errors)
            instance.set_password(password)
        return super(UserSerializer, self).update(instance, validated_data)

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email',
            'tel',
            'avatar',
            'first_name',
            'last_name',
            'full_name',
            'role',
            'status',
            'created_at',
            'updated_at',
            # Write only fields
            'password',
            'password_confirmation',
            'current_password',
        )
        read_only_fields = (
            'id',
            'full_name',
            'role',
            'status',
            'created_at',
            'updated_at',
        )
