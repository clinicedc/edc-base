import arrow

from datetime import date

from django.core.exceptions import ValidationError

from edc_base.exceptions import FutureDateError
from edc_base.utils import get_utcnow
from django.conf import settings
from edc_base.model.validators.date import date_not_future


def dob_not_future(value):
    try:
        date_not_future(value)
    except FutureDateError:
        raise FutureDateError(u'Date of birth cannot be a future date. You entered {}.'.format(value))


def dob_not_today(value):
    now = date.today()
    if now == value:
        raise ValidationError(u'Date of birth cannot be today. You entered {}.'.format(value))
