import pytz

from datetime import timedelta
from django.utils import timezone

from django.core.exceptions import ValidationError
from django.conf import settings
from django.utils.timezone import make_aware, make_naive

tz = pytz.timezone(settings.TIME_ZONE)


def my_make_naive(value, tz):
    try:
        value = make_naive(value, tz)
    except ValueError:
        pass
    return value


def my_make_aware(value, tz):
    try:
        value = make_aware(value, tz)
    except ValueError:
        pass
    return value


def datetime_not_future(value):
    value = my_make_aware(value, tz)
    now = my_make_aware(timezone.now(), tz)
    time_error = timedelta(minutes=10)
    if value > now + time_error:
        raise ValidationError(u'Datetime cannot be a future date and time. You entered {}'.format(value))


def date_not_future(value):
    now = timezone.now().date()
    if value > now:
        raise ValidationError(u'Date cannot be a future date. You entered {}'.format(value))


def datetime_is_future(value):
    value = my_make_aware(value, tz)
    time_error = timedelta(minutes=10)
    if value < timezone.now() + time_error:
        raise ValidationError(u'Datetime must be a future date and time. You entered {}'.format(value))


def date_is_future(value):
    now = timezone.now().date()
    if value < now:
        raise ValidationError(u'Date must be a future date. You entered {}'.format(value))
