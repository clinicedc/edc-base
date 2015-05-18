import re

from django.forms import ValidationError

from edc.core.crypto_fields.fields import EncryptedIdentityField


class EncryptedOmangField(EncryptedIdentityField):

    def validate_with_cleaned_data(self, attname, cleaned_data):
        """ Tests the OMANG, this field validator must have access to the keys identity_type, gender """
        if attname in cleaned_data:
            value = cleaned_data.get(attname, None)
            if value:
                # check for required keys from cleaned_data
                if 'identity_type' not in cleaned_data:
                    raise TypeError('EncryptedOmangField expects key \'identity_type\' for validation')
                if 'gender' not in cleaned_data:
                    raise TypeError('EncryptedOmangField expects key \'gender\' for validation')
                # check if value is encrypted, if so we need to decrypt it to run the tests
                if self.is_encrypted(value):
                    self.decrypt(value)
                if not self.is_encrypted(value):
                    gender = cleaned_data.get('gender', None)
                    identity_type = cleaned_data.get('identity_type', None)
                    if value:
                        if identity_type == 'OMANG' and gender in ['M', 'F']:
                            # the OMANG uses the format below which ties it to the gender on digit 5.
                            # the OMANG digits have no other known meaning.
                            str_value = "%s" % (value)
                            pattern = {'M': '^[0-9]{4}[1]{1}[0-9]{4}$', 'F': '^[0-9]{4}[2]{1}[0-9]{4}$'}
                            p = re.compile(pattern[gender])
                            if not p.match(str_value):
                                raise ValidationError(u'Invalid Omang number format and/or invalid Omang format for gender (%s). You entered %s.' % (gender, str_value))
