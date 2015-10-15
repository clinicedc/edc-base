from distutils.version import StrictVersion
from django import get_version
from django.utils.translation import ugettext as _
from django_extensions.db.fields import UUIDField

if StrictVersion(get_version()) >= StrictVersion('1.8.0'):
    raise ImportError('This module expects version < Django 1.8.0, Got {}'.format(get_version()))


class UUIDAutoField(UUIDField):
    """
    This is not technically an AutoField as the DB does not provide the value. A django AutoField
    lets the DB provide the value in base.py (save_base). To avoid that happening here, this
    field inherits from UUIDField->CharField->Field instead of AutoField->Field.
    """
    description = _("UuidAutoField")

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('primary_key', True)
        UUIDField.__init__(self, *args, **kwargs)

    def south_field_triple(self):
        "Returns a suitable description of this field for South."
        # We'll just introspect the _actual_ field.
        from south.modelsinspector import introspector
        field_class = "django.db.models.fields.CharField"
        args, kwargs = introspector(self)
        # That's our definition!
        return (field_class, args, kwargs)
