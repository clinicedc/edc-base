from dateutil.relativedelta import relativedelta
from datetime import datetime, time, date


def age(born, reference_date):
    if not born:
        raise ValueError('DOB cannot be None.')
    elif born > reference_date:
        raise ValueError('Reference date precedes DOB.')
    return relativedelta(reference_date, born)


def formatted_age(born, reference_date=None):
    reference_date = reference_date or date.today()
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


def get_age_in_days(reference_date, dob):
    dob = datetime.combine(dob, time())
    tdelta = reference_date - dob
    return tdelta.days
