from datetime import timedelta
from django.utils import timezone

from django.core.exceptions import ValidationError
from django.conf import settings

study_open_datetime = getattr(settings, 'STUDY_OPEN_DATETIME')


def datetime_not_future(value):
    time_error = timedelta(minutes=10)
    if value > timezone.now() + time_error:
        raise ValidationError(u'Date cannot be a future date and time. You entered %s'.format(value))


def date_not_future(value):
    now = timezone.now().date()
    if value > now:
        raise ValidationError(u'Date cannot be a future date. You entered %s'.format(value))


def datetime_is_future(value):
    time_error = timedelta(minutes=10)
    if value < timezone.now() + time_error:
        raise ValidationError(u'Date must be a future date and time. You entered %s'.format(value))


def date_is_future(value):
    now = timezone.now().date()
    if value < now:
        raise ValidationError(u'Date must be a future date. You entered %s'.format(value))


def datetime_is_after_consent(value):
    """ not working..."""
    now = value
    if value != now:
        raise ValidationError(u'Date and time cannot be prior to consent date. You entered %s'.format(value))


def date_not_before_study_start(value_date):
    value_datetime = timezone.datetime(value_date.year, value_date.month, value_date.day, 0, 0)
    if value_datetime < study_open_datetime:
        raise ValidationError(
            'Invalid date. Study opened on {}. Got {}.'.format(study_open_datetime, value_date))


def datetime_not_before_study_start(value_datetime):
    if value_datetime < study_open_datetime:
        raise ValidationError(
            'Invalid date. Study opened on {}. Got {}.'.format(study_open_datetime, value_datetime))
