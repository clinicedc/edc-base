import socket

from django.db.models import CharField
from django.utils.translation import ugettext as _


class HostnameModificationField (CharField):
    """
    HostnameModificationField

    By default, sets editable=False, blank=True, default=socket.gethostname()

    Sets value to socket.gethostname() on each save of the model.
    """
    description = _("Custom field for hostname modified")

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('editable', False)
        kwargs.setdefault('blank', True)
        kwargs.setdefault('max_length', 50)
        kwargs.setdefault('verbose_name', 'Hostname')
        kwargs.setdefault('default', socket.gethostname())
        CharField.__init__(self, *args, **kwargs)

    def pre_save(self, model, add):
        value = socket.gethostname()
        setattr(model, self.attname, value)
        return value

    def get_internal_type(self):
        return "CharField"

    def south_field_triple(self):
        "Returns a suitable description of this field for South."
        # We'll just introspect ourselves, since we inherit.
        from south.modelsinspector import introspector
        field_class = "django.db.models.fields.CharField"
        args, kwargs = introspector(self)
        return (field_class, args, kwargs)
