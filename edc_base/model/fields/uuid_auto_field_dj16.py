from django import get_version
from django.utils.translation import ugettext as _
from django_extensions.db.fields import UUIDField

if not get_version().startswith('1.6'):
    raise ImportError('This module requires Django 1.6')


class UUIDAutoField(UUIDField):
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
