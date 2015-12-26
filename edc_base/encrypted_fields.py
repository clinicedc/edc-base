import six
from distutils.version import StrictVersion
from django import get_version
from django.conf import settings

from edc_base.model.fields import IdentityTypeField
from edc_base.model.fields import IsDateEstimatedField
from django.core.exceptions import ImproperlyConfigured

try:
    import django_crypto_fields
    if 'django_crypto_fields' not in settings.INSTALLED_APPS:
        raise ImproperlyConfigured(
            'Why is the package \'django_crypto_fields\' installed? '
            'Choosing the wrong encryption package can lead to data loss. '
            'If you mean to use it, add it to INSTALLED_APPS, otherwise uninstall it '
            'with \'pip uninstall django_crypto_fields\'.')
except ImportError:
    pass


if StrictVersion(get_version()) < StrictVersion('1.8.0') and six.PY2:
    try:
        from edc.core.crypto_fields.classes import FieldCryptor
        from edc.core.crypto_fields.fields import (
            EncryptedFirstnameField as FirstnameField,
            EncryptedLastnameField as LastnameField,
            EncryptedCharField, EncryptedTextField,
            EncryptedIdentityField as IdentityField,
            EncryptedDecimalField, BaseEncryptedField)
    except ImportError as e:
        print(e)
        from django_crypto_fields.classes import FieldCryptor
        from django_crypto_fields.fields import (
            FirstnameField, LastnameField, EncryptedCharField, EncryptedTextField, IdentityField)
else:
    from django_crypto_fields.classes import FieldCryptor
    # from django_crypto_fields.utils import mask_encrypted
    from django_crypto_fields.fields import (
        FirstnameField, LastnameField, EncryptedCharField, EncryptedTextField, IdentityField,
        BaseField as BaseEncryptedField)


def mask_encrypted(value):
    return FieldCryptor('rsa', 'local').mask(value)
