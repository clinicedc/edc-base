import os
import pwd

from django.db.models import CharField
from django.utils.translation import ugettext as _


class UserField(CharField):

    description = _("Custom field for user created")

    def get_os_username(self):
        return pwd.getpwuid(os.getuid()).pw_name

    def pre_save(self, model_instance, add):
        """Updates username created on ADD only."""
        value = super(UserField, self).pre_save(model_instance, add)
        if not value and not add:
            # fall back to OS user if not accessing through browser
            # better than nothing ...
            value = self.get_os_username()
            setattr(model_instance, self.attname, value)
            return value
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
