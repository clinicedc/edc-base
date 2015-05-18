import socket

from django.db.models import CharField
from django.utils.translation import ugettext as _


class HostnameCreationField (CharField):
    """
    HostnameCreationField

    By default, sets editable=False, blank=True, default=socket.gethostname()
    """

    description = _("Custom field for hostname created")

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('editable', False)
        kwargs.setdefault('blank', True)
        kwargs.setdefault('max_length', 50)
        kwargs.setdefault('verbose_name', 'Hostname')
        kwargs.setdefault('default', socket.gethostname())
        CharField.__init__(self, *args, **kwargs)

    def get_internal_type(self):
        return "CharField"

    def south_field_triple(self):
        "Returns a suitable description of this field for South."
        # We'll just introspect ourselves, since we inherit.
        from south.modelsinspector import introspector
        field_class = "django.db.models.fields.CharField"
        args, kwargs = introspector(self)
        return (field_class, args, kwargs)
