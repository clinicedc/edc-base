import arrow

from datetime import timedelta

from edc_base.exceptions import FutureDateError, NotFutureDateError


def datetime_not_future(value):
    value_utc = arrow.Arrow.fromdatetime(value, value.tzinfo).to('utc').datetime
    time_error = timedelta(minutes=10)
    if value_utc > arrow.utcnow() + time_error:
        raise FutureDateError(u'Datetime cannot be a future date and time. You entered {}'.format(value))


def date_not_future(value):
    value_utc = arrow.Arrow.fromdatetime(value, value.tzinfo).to('utc').date
    if value_utc > arrow.utcnow().date():
        raise FutureDateError(u'Date cannot be a future date. You entered {}'.format(value))


def datetime_is_future(value):
    value_utc = arrow.Arrow.fromdatetime(value, value.tzinfo).to('utc').datetime
    time_error = timedelta(minutes=10)
    if value_utc < arrow.utcnow() + time_error:
        raise NotFutureDateError(u'Datetime must be a future date and time. You entered {}'.format(value))


def date_is_future(value):
    value_utc = arrow.Arrow.fromdatetime(value, value.tzinfo).to('utc').date
    if value_utc < arrow.utcnow().date():
        raise NotFutureDateError(u'Date must be a future date. You entered {}'.format(value))
