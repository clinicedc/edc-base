import six

from django import get_version

if get_version().startswith('1.6') and six.PY2:
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
        from edc.core.crypto_fields.utils import mask_encrypted
    except ImportError as e:
        print(e)
        from edc_base.model.fields import IdentityTypeField
        from edc_base.model.fields import IsDateEstimatedField
        from django_crypto_fields.classes import FieldCryptor
        from django_crypto_fields.utils import mask_encrypted
        from django_crypto_fields.fields import (
            FirstnameField, LastnameField, EncryptedCharField, EncryptedTextField, IdentityField)
else:
    from edc_base.model.fields import IdentityTypeField
    from edc_base.model.fields import IsDateEstimatedField
    from django_crypto_fields.classes import FieldCryptor
    from django_crypto_fields.utils import mask_encrypted
    from django_crypto_fields.fields import (
        FirstnameField, LastnameField, EncryptedCharField, EncryptedTextField, IdentityField)
