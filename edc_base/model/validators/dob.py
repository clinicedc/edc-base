from datetime import date

from django.core.exceptions import ValidationError


def dob_not_future(value):
    now = date.today()
    if now < value:
        raise ValidationError(u'Date of birth cannot be a future date. You entered {}.'.format(value))


def dob_not_today(value):
    now = date.today()
    if now == value:
        raise ValidationError(u'Date of birth cannot be today. You entered {}.'.format(value))
