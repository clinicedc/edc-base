from django.core.exceptions import ValidationError

from django.conf import settings


def GenderOfConsent(value):
    gender_list = [s for s in settings.GENDER_OF_CONSENT]
    if value not in gender_list:
        raise ValidationError(u'Gender of consent not in {}. You entered {}.'.format(gender_list, value))
