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


if 'edc_crypto_fields' in settings.INSTALLED_APPS:
        import M2Crypto

try:
    from edc_crypto_fields.classes import FieldCryptor
    from edc_crypto_fields.fields import (
        EncryptedFirstnameField as FirstnameField,
        EncryptedLastnameField as LastnameField,
        EncryptedCharField, EncryptedTextField,
        EncryptedIdentityField as IdentityField,
        EncryptedDecimalField, BaseEncryptedField)
    # from edc_crypto_fields.models import Crypt  # causes import error
except ImportError as e:
    from django_crypto_fields.classes import FieldCryptor
    from django_crypto_fields.fields import (
        FirstnameField, LastnameField, EncryptedCharField, EncryptedTextField, IdentityField,
        BaseField as BaseEncryptedField)


def mask_encrypted(value):
    return FieldCryptor('rsa', 'local').mask(value)
