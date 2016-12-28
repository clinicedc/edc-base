from datetime import timedelta

from edc_base.exceptions import FutureDateError, NotFutureDateError

from ...utils import get_utcnow


def datetime_not_future(value):
    time_error = timedelta(minutes=10)
    if value > get_utcnow() + time_error:
        raise FutureDateError(u'Datetime cannot be a future date and time. You entered {}'.format(value))


def date_not_future(value):
    now = get_utcnow().date()
    if value > now:
        raise FutureDateError(u'Date cannot be a future date. You entered {}'.format(value))


def datetime_is_future(value):
    time_error = timedelta(minutes=10)
    if value < get_utcnow() + time_error:
        raise NotFutureDateError(u'Datetime must be a future date and time. You entered {}'.format(value))


def date_is_future(value):
    now = get_utcnow().date()
    if value < now:
        raise NotFutureDateError(u'Date must be a future date. You entered {}'.format(value))
