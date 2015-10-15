import six
from distutils.version import StrictVersion
from django import get_version

if StrictVersion(get_version()) < StrictVersion('1.8.0') and six.PY2:
    try:
        from edc.core.crypto_fields.fields import (
            EncryptedFirstnameField as FirstnameField,
            EncryptedLastnameField as LastnameField,
            EncryptedCharField, EncryptedTextField,
            EncryptedIdentityField as IdentityField,
            EncryptedDecimalField)
        from edc.base.model.fields import IdentityTypeField
        from edc.base.model.fields import IsDateEstimatedField
        from edc.core.crypto_fields.classes import FieldCryptor
        # from edc.core.crypto_fields.utils import mask_encrypted
    except ImportError as e:
        print(e)
        from edc_base.model.fields import IdentityTypeField
        from edc_base.model.fields import IsDateEstimatedField
        from django_crypto_fields.classes import FieldCryptor
        # from django_crypto_fields.utils import mask_encrypted
        from django_crypto_fields.fields import (
            FirstnameField, LastnameField, EncryptedCharField, EncryptedTextField, IdentityField)
else:
    from edc_base.model.fields import IdentityTypeField
    from edc_base.model.fields import IsDateEstimatedField
    from django_crypto_fields.classes import FieldCryptor
    # from django_crypto_fields.utils import mask_encrypted
    from django_crypto_fields.fields import (
        FirstnameField, LastnameField, EncryptedCharField, EncryptedTextField, IdentityField)


def mask_encrypted(value):
    return FieldCryptor('rsa', 'local').mask(value)
