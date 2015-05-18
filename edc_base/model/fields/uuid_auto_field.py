# from django_extensions.db.fields import UUIDField
from django.db.models import UUIDField
from django.utils.translation import ugettext as _


class UUIDAutoField(UUIDField):
    """
    This is not technically an AutoField as the DB does not provide the value. A django AutoField
    lets the DB provide the value in base.py (save_base). To avoid that happening here, this
    field inherits from UUIDField->CharField->Field instead of AutoField->Field.

    """
    description = _("UuidAutoField")

    def __init__(self, *args, **kwargs):
        assert kwargs.get('primary_key', False) is True, "%ss must have primary_key=True." % self.__class__.__name__
        super(UUIDAutoField, self).__init__(*args, **kwargs)
