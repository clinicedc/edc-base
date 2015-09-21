from django import get_version
from .custom_fields import (
    IdentityTypeField, InitialsField, IsDateEstimatedField, DobField, OtherCharField)
from .hostname_modification_field import HostnameModificationField
from .userfield import UserField

try:
    from .uuid_auto_field_dj16 import UUIDAutoField, UUIDField
except ImportError:
    from .uuid_auto_field import UUIDAutoField, UUIDField
