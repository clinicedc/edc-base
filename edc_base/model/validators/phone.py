import re

from django.conf import settings
from django.core.exceptions import ValidationError


def phone_number(value, pattern, word):
    str_value = "%s" % (value)
    p = re.compile(pattern)
    if not p.match(str_value):
        raise ValidationError(u'Invalid {} number. Got {}.'.format(word, str_value))


def CellNumber(value):
    """
        sample for BW:
            CELLPHONE_REGEX = '^[7]{1}[12345678]{1}[0-9]{6}$'
    """
    try:
        regex = settings.CELLPHONE_REGEX
    except AttributeError:
        regex = '^[0-9+\(\)#\.\s\/ext-]+$'
    phone_number(value, regex, 'cell')


def TelephoneNumber(value):
    """
        sample for BW:
            TELEPHONE_REGEX = '^[2-8]{1}[0-9]{6}$'
    """
    try:
        regex = settings.TELEPHONE_REGEX
    except AttributeError:
        regex = '^[0-9+\(\)#\.\s\/ext-]+$'
    phone_number(value, regex, 'telephone')
