import arrow

from datetime import timedelta

from django.core.exceptions import ValidationError
from django.utils.timezone import get_default_timezone


def datetime_not_future(value):
    value_utc = arrow.Arrow.fromdatetime(value, value.tzinfo).to('utc').datetime
    time_error = timedelta(minutes=10)
    if value_utc > arrow.utcnow() + time_error:
        raise ValidationError('Cannot be a future date')


def date_not_future(value):
    value_utc = arrow.Arrow.fromdate(value, tzinfo=get_default_timezone()).to('utc').date()
    if value_utc > arrow.utcnow().date():
        raise ValidationError('Cannot be a future date')


def datetime_is_future(value):
    value_utc = arrow.Arrow.fromdatetime(value, value.tzinfo).to('utc').datetime
    time_error = timedelta(minutes=10)
    if value_utc < arrow.utcnow() + time_error:
        raise ValidationError('Expected a future date')


def date_is_future(value):
    value_utc = arrow.Arrow.fromdate(value, tzinfo=get_default_timezone()).to('utc').date()
    if value_utc < arrow.utcnow().date():
        raise ValidationError('Expected a future date')
