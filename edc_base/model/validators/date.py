import pytz
from datetime import timedelta, datetime
from django.utils import timezone

from django.core.exceptions import ValidationError
from django.conf import settings
from django.utils.timezone import make_aware, is_naive, make_naive

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


def get_study_open_datetime():
    study_open_datetime = settings.STUDY_OPEN_DATETIME
    if settings.USE_TZ:
        study_open_datetime = my_make_aware(settings.STUDY_OPEN_DATETIME, tz)
    else:
        study_open_datetime = my_make_naive(study_open_datetime, tz)
    return study_open_datetime


def datetime_not_future(value):
    if settings.USE_TZ:
        value = my_make_aware(value, tz)
    time_error = timedelta(minutes=10)
    if value > timezone.now() + time_error:
        raise ValidationError(u'Datetime cannot be a future date and time. You entered {}'.format(value))


def date_not_future(value):
    now = timezone.now().date()
    if value > now:
        raise ValidationError(u'Date cannot be a future date. You entered {}'.format(value))


def datetime_is_future(value):
    if settings.USE_TZ:
        value = my_make_aware(value, tz)
    time_error = timedelta(minutes=10)
    if value < timezone.now() + time_error:
        raise ValidationError(u'Datetime must be a future date and time. You entered {}'.format(value))


def date_is_future(value):
    now = timezone.now().date()
    if value < now:
        raise ValidationError(u'Date must be a future date. You entered {}'.format(value))


def date_not_before_study_start(value):
    if settings.USE_TZ:
        value_datetime = my_make_aware(
            datetime(value.year, value.month, value.day, 0, 0), tz)
    else:
        value_datetime = datetime(value.year, value.month, value.day, 0, 0)
    study_open_datetime = get_study_open_datetime()
    if value_datetime < study_open_datetime:
        raise ValidationError(
            'Invalid date. Study opened on {}. Got {}.'.format(study_open_datetime, value_datetime))


def datetime_not_before_study_start(value):
    if settings.USE_TZ:
        value = my_make_aware(value, tz)
    study_open_datetime = get_study_open_datetime()
    if value < study_open_datetime:
        raise ValidationError(
            'Invalid date. Study opened on {}. Got {}.'.format(study_open_datetime, value))
