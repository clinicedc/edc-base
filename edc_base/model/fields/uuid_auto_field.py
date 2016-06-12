import uuid

from django.db.models import AutoField
from django.utils.translation import ugettext as _
from django.core import exceptions


class UUIDAutoField(AutoField):
    """ AutoField for Universally unique identifier.

    Follows closely with django UUIDField, however, subclasses AutoField
    instead of UUIDField since apps such as simple_history expect
    the auto field to be an instance of AutoField.

    Inserts a randomly generated UUID value in pre_save instead of expecting the auto
    value to come from the DB backend.
    """
    default_error_messages = {
        'invalid': _("'%(value)s' is not a valid UUID."),
    }
    description = 'AutoField for Universally unique identifier'
    empty_strings_allowed = False

    def __init__(self, verbose_name=None, **kwargs):
        kwargs['max_length'] = 32
        kwargs['help_text'] = "System auto field. UUID primary key."
        kwargs['default'] = uuid.uuid4
        super(UUIDAutoField, self).__init__(verbose_name, **kwargs)
        # self.default = uuid.uuid4

    def deconstruct(self):
        name, path, args, kwargs = super(UUIDAutoField, self).deconstruct()
        del kwargs['max_length']
        del kwargs['help_text']
        del kwargs['default']
        kwargs['primary_key'] = True
        return name, path, args, kwargs

    def get_internal_type(self):
        return "UUIDField"

#     def pre_save(self, model_instance, add):
#         value = super(UUIDAutoField, self).pre_save(model_instance, add)
#         if add and value is None:
#             value = uuid.uuid4()
#             setattr(model_instance, self.attname, value)
#         else:
#             if not value:
#                 value = uuid.uuid4()
#                 setattr(model_instance, self.attname, value)
#         return value

    def validate(self, value, model_instance):
        pass

    def get_db_prep_value(self, value, connection, prepared=False):
        if value is None:
            return None
        if not isinstance(value, uuid.UUID):
            try:
                value = uuid.UUID(value)
            except AttributeError:
                raise TypeError(self.error_messages['invalid'] % {'value': value})

        if connection.features.has_native_uuid_field:
            return value
        return value.hex

    def get_prep_value(self, value):
        value = super(UUIDAutoField, self).get_prep_value(value)
        if value is None:
            return None
        return value

    def to_python(self, value):
        if value and not isinstance(value, uuid.UUID):
            try:
                return uuid.UUID(value)
            except ValueError:
                raise exceptions.ValidationError(
                    self.error_messages['invalid'],
                    code='invalid',
                    params={'value': value},
                )
        return value
