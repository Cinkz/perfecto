from __future__ import unicode_literals

from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible


@deconstructible
class ListValidator(object):
    def __init__(self, code=None, message=None, child=None):
        if code is not None:
            self.code = code
        else:
            self.code = 'list_required'
        if message is not None:
            self.message = message
        else:
            self.message = 'Value has to be a list.'
        if child is not None:
            if not isinstance(child, type):
                raise TypeError('child should be a type.')
            self.child = child
        else:
            self.child = dict

    def __call__(self, value):
        if not isinstance(value, list):
            raise ValidationError(code=self.code, message=self.message)

        for item in value:
            if not isinstance(item, self.child):
                raise ValidationError(code=self.code, message=self.message)

    def __eq__(self, other):
        return (
            isinstance(other, ListValidator) and
            (self.message == other.message) and
            (self.code == other.code) and
            (self.child == other.child)
        )

    def __ne__(self, other):
        return not self == other
