from uuid import uuid4

from django.db.models import UUIDField
from django.utils.translation import ugettext as _


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
