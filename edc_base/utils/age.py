import pytz

from dateutil.relativedelta import relativedelta

from django.utils import timezone

tz = pytz.timezone('UTC')


def age(born, reference_datetime):
    """Age is local."""
    if not born:
        raise ValueError('DOB cannot be None.')
    reference_date = timezone.localtime(reference_datetime).date()
    if relativedelta(born, reference_date) > 0:
        raise ValueError('Reference date precedes DOB.')
    return relativedelta(born, reference_date)


def formatted_age(born, reference_datetime=None):
    reference_datetime = reference_datetime or timezone.now()
    reference_date = timezone.localtime(reference_datetime).date()
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
    reference_date = timezone.localtime(reference_datetime).date()
    rdelta = relativedelta(reference_date, dob)
    return rdelta.days
