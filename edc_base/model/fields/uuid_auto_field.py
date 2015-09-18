from uuid import uuid4
from django import get_version
from django.utils.translation import ugettext as _

__all__ = ['UUIDAutoField']


if get_version().startswith('1.6'):

    from django_extensions.db.fields import UUIDField

    class UUIDAutoField (UUIDField):
        """
        This is not technically an AutoField as the DB does not provide the value. A django AutoField
        lets the DB provide the value in base.py (save_base). To avoid that happening here, this
        field inherits from UUIDField->CharField->Field instead of AutoField->Field.
        """
        description = _("UuidAutoField")

        def __init__(self, *args, **kwargs):
            assert kwargs.get('primary_key', False) is True, "%ss must have primary_key=True." % self.__class__.__name__
            UUIDField.__init__(self, *args, **kwargs)

        def south_field_triple(self):
            "Returns a suitable description of this field for South."
            # We'll just introspect the _actual_ field.
            from south.modelsinspector import introspector
            field_class = "django.db.models.fields.CharField"
            args, kwargs = introspector(self)
            # That's our definition!
            return (field_class, args, kwargs)

else:

    from django.db.models import UUIDField

    class UUIDAutoField(UUIDField):
        """ UUIDField

        modified / simplified from django_extensions

        Uses UUID version 4 (randomly generated UUID).
        """

        description = _("UuidAutoField")

        def create_uuid(self):
            return uuid4()

        def pre_save(self, model_instance, add):
            value = super(UUIDField, self).pre_save(model_instance, add)
            if add and value is None:
                value = self.create_uuid()
                setattr(model_instance, self.attname, value)
            else:
                if not value:
                    value = self.create_uuid()
                    setattr(model_instance, self.attname, value)
            return value

        def formfield(self, **kwargs):
            return None

        def south_field_triple(self):
            "Returns a suitable description of this field for South."
            # We'll just introspect the _actual_ field.
            from south.modelsinspector import introspector
            # field_class = "django.db.models.fields.CharField"
            field_class = "django.db.models.fields.UUIDField"
            args, kwargs = introspector(self)
            # That's our definition!
            return (field_class, args, kwargs)
