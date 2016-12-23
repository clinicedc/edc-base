import arrow
from dateutil import tz
import pytz
import random
import re
from uuid import uuid4

from datetime import datetime
from dateutil.relativedelta import relativedelta
from decimal import Decimal, InvalidOperation
from math import ceil

from django.conf import settings
from django.utils.encoding import force_text
from django.utils.timezone import localtime
from django.core.exceptions import ImproperlyConfigured
from git.refs import reference
from edc_base.exceptions import AgeValueError

safe_allowed_chars = 'ABCDEFGHKMNPRTUVWXYZ2346789'


class MyTimezone:
    def __init__(self, timezone):
        if timezone:
            self.timezone = tz.gettz(timezone)
        else:
            try:
                self.timezone = tz.gettz(settings.BORN_TZ_DEFAULT)
            except AttributeError:
                self.timezone = None


class ConvertError(Exception):
    pass


def get_uuid():
    return str(uuid4())


def round_up(value, digits):
    ceil(value * (10 ** digits)) / (10 ** digits)


def get_safe_random_string(length=12, safe=None, allowed_chars=None):
    safe = True if safe is None else safe
    allowed_chars = (allowed_chars or
                     'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRTUVWXYZ012346789!@#%^&*()?<>.,[]{}')
    if safe:
        allowed_chars = 'ABCDEFGHKMNPRTUVWXYZ2346789'
    return ''.join([random.choice(allowed_chars) for _ in range(length)])


def get_utcnow():
    return arrow.utcnow().datetime


def to_utc(dt, birth_tz=None):
    """Returns a datetime after converting date or datetime from given timezone to UTC."""
    try:
        dt.date()
    except AttributeError:
        # handle born as date
        utc = arrow.Arrow.fromdate(dt, tzinfo=birth_tz).to('UTC')
    else:
        # handle born as datetime
        if birth_tz:
            raise ValueError('timezone specified for aware datetime. Got birth_tz={}'.format(birth_tz))
        utc = arrow.Arrow.fromdatetime(dt, tzinfo=dt.tzinfo).to('utc')
    return utc


def age(born, reference_dt, birth_tz=None):
    """Returns a relative delta"""
    # avoid null dates/datetimes
    if not born:
        raise ValueError('born cannot be None.')
    if not reference_dt:
        raise ValueError('reference_dt cannot be None.')
    # convert dates or datetimes to UTC datetimes
    birth_tz = MyTimezone(birth_tz).timezone
    born_utc = to_utc(born, birth_tz)
    reference_dt_utc = to_utc(reference_dt, birth_tz)
    rdelta = relativedelta(reference_dt_utc.datetime, born_utc.datetime)
    if born_utc.datetime > reference_dt_utc.datetime:
        raise AgeValueError(
            'Reference date {} {} precedes DOB {} {}. Got {}'.format(
                reference_dt, str(reference_dt.tzinfo), born, birth_tz, rdelta))
    return rdelta


def formatted_age(born, reference_dt=None, birth_tz=None):
    if born:
        born = arrow.Arrow.fromdate(born, tzinfo=birth_tz).datetime
        reference_dt = reference_dt or get_utcnow()
        age_delta = age(born, reference_dt or get_utcnow())
        if born > reference_dt:
            return '?'
        elif age_delta.years == 0 and age_delta.months <= 0:
            return '%sd' % (age_delta.days)
        elif age_delta.years == 0 and age_delta.months > 0 and age_delta.months <= 2:
            return '%sm%sd' % (age_delta.months, age_delta.days)
        elif age_delta.years == 0 and age_delta.months > 2:
            return '%sm' % (age_delta.months)
        elif age_delta.years == 1:
            m = age_delta.months + 12
            return '%sm' % (m)
        elif age_delta.years > 1:
            return '%sy' % (age_delta.years)
        else:
            raise TypeError(
                'Age template tag missed a case... today - born. '
                'rdelta = {} and {}'.format(age_delta, born))


def get_age_in_days(reference_datetime, dob):
    age_delta = age(dob, reference_datetime)
    return age_delta.days


def convert_from_camel(name):
    """Converts from camel case to lowercase divided by underscores."""
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


class Convert(object):

    def __init__(self, value, convert=None, time_format=None):
        self.value = value
        self.convert = False if convert is False else True
        self.time_format = time_format or '%H:%M'

    def to_value(self):
        """Converts a string representation of a value into its original datatype.

        For dates and datetimes always returns a time zone aware datetime."""
        string_value = self.value.strip(' "')
        if self.convert:
            try:
                return self.to_time(string_value)
            except ConvertError:
                pass
            try:
                return self.to_boolean(string_value)
            except ConvertError:
                pass
            try:
                return self.to_decimal(string_value)
            except ConvertError:
                pass
            try:
                return self.to_int(string_value)
            except ConvertError:
                pass
            try:
                return self.to_datetime(string_value)
            except ConvertError:
                pass
            # raise ConvertError('Cannot convert string to value. Got \'{}\''.format(self.value))
        return string_value

    def to_string(self):
        try:
            string_value = self.value.isoformat()
            try:
                self.value.time()
                string_value = '{} {}'.format(string_value, self.value.strftime(self.time_format))
            except AttributeError:
                pass
        except AttributeError:
            string_value = str(self.value)
        return string_value or force_text(self.value)

    def to_time(self, string_value):
        if re.match('^[0-9]{1,2}\:[0-9]{2}$', string_value):
            return string_value
        else:
            raise ConvertError()

    def to_boolean(self, string_value):
        if string_value.lower() in ['true', 'false', 'none']:
            return eval(string_value)
        else:
            raise ConvertError()

    def to_decimal(self, string_value):
        if '.' in string_value:
            try:
                value = Decimal(string_value)
                if str(value) == string_value:
                    return value
            except ValueError:
                pass
            except InvalidOperation:
                pass
        raise ConvertError()

    def to_int(self, string_value):
        try:
            value = int(string_value)
            if str(value) == string_value:
                return value
        except ValueError:
            pass
        raise ConvertError()
