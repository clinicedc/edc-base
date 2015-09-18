import socket

from django.db.models import CharField
from django.utils.translation import ugettext as _


class HostnameModificationField (CharField):

    description = _("Custom field for hostname modified")

    def pre_save(self, model_instance, add):
        """Updates socket.gethostname() on each save."""
        value = socket.gethostname()
        setattr(model_instance, self.attname, value)
        return value

    def get_internal_type(self):
        return "CharField"

    def south_field_triple(self):
        "Returns a suitable description of this field for South."
        # We'll just introspect the _actual_ field.
        from south.modelsinspector import introspector
        field_class = "django.db.models.fields.CharField"
        args, kwargs = introspector(self)
        # That's our definition!
        return (field_class, args, kwargs)
