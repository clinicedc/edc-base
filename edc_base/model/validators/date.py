from datetime import timedelta
from django.utils import timezone

from django.core.exceptions import ValidationError


def datetime_not_future(value):
    time_error = timedelta(minutes=10)
    if value > timezone.now() + time_error:
        raise ValidationError(u'Datetime cannot be a future date and time. You entered {}'.format(value))


def date_not_future(value):
    now = timezone.now().date()
    if value > now:
        raise ValidationError(u'Date cannot be a future date. You entered {}'.format(value))


def datetime_is_future(value):
    time_error = timedelta(minutes=10)
    if value < timezone.now() + time_error:
        raise ValidationError(u'Datetime must be a future date and time. You entered {}'.format(value))


def date_is_future(value):
    now = timezone.now().date()
    if value < now:
        raise ValidationError(u'Date must be a future date. You entered {}'.format(value))
