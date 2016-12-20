import pytz
import random
import re
from uuid import uuid4

from datetime import datetime, time
from dateutil.relativedelta import relativedelta
from decimal import Decimal, InvalidOperation
from math import ceil

from django.utils.encoding import force_text
from django.utils.timezone import localtime

safe_allowed_chars = 'ABCDEFGHKMNPRTUVWXYZ2346789'


class ConvertError(Exception):
    pass


def get_uuid():
    return str(uuid4())


def get_utcnow():
    return datetime.now(tz=pytz.utc)


def round_up(value, digits):
    ceil(value * (10 ** digits)) / (10 ** digits)


def get_safe_random_string(length=12, safe=None, allowed_chars=None):
    safe = True if safe is None else safe
    allowed_chars = (allowed_chars or
                     'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRTUVWXYZ012346789!@#%^&*()?<>.,[]{}')
    if safe:
        allowed_chars = 'ABCDEFGHKMNPRTUVWXYZ2346789'
    return ''.join([random.choice(allowed_chars) for _ in range(length)])


def age(born, reference_dt):
    """Returns a relative delta"""
    if not born:
        raise ValueError('DOB cannot be None.')
    try:
        born.date()
    except AttributeError as e:
        born = datetime.combine(born, time())
    try:
        born = pytz.utc.localize(born)
    except ValueError as e:
        if 'tzinfo is already set' in str(e):
            pass
    born = localtime(born)
    if not reference_dt:
        reference_dt = localtime(get_utcnow())
    else:
        try:
            reference_dt.date()
        except AttributeError:
            reference_dt = datetime.combine(reference_dt, time())
        try:
            reference_dt = pytz.utc.localize(reference_dt)
        except ValueError as e:
            if 'tzinfo is already set' in str(e):
                pass
    reference_dt = localtime(reference_dt)
    if born > reference_dt:
        rdelta = relativedelta(reference_dt, born)
        raise ValueError('Reference date {} precedes DOB {}. Got {}'.format(reference_dt, born, rdelta))
    return relativedelta(reference_dt, born)


def formatted_age(born, reference_datetime=None):
    reference_datetime = reference_datetime or get_utcnow()
    reference_date = localtime(reference_datetime).date()
    if born:
        rdelta = relativedelta(reference_date, born)
        if born > reference_date:
            return '?'
        elif rdelta.years == 0 and rdelta.months <= 0:
            return '%sd' % (rdelta.days)
        elif rdelta.years == 0 and rdelta.months > 0 and rdelta.months <= 2:
            return '%sm%sd' % (rdelta.months, rdelta.days)
        elif rdelta.years == 0 and rdelta.months > 2:
            return '%sm' % (rdelta.months)
        elif rdelta.years == 1:
            m = rdelta.months + 12
            return '%sm' % (m)
        elif rdelta.years > 1:
            return '%sy' % (rdelta.years)
        else:
            raise TypeError(
                'Age template tag missed a case... today - born. '
                'rdelta = {} and {}'.format(rdelta, born))


def get_age_in_days(reference_datetime, dob):
    reference_date = localtime(reference_datetime).date()
    rdelta = relativedelta(reference_date, dob)
    return rdelta.days


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
