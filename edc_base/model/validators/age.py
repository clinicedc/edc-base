from datetime import date
from dateutil.relativedelta import relativedelta

from django.conf import settings
from django.core.exceptions import ValidationError

min_age_of_consent = getattr(settings, 'MIN_AGE_OF_CONSENT', 18)
max_age_of_consent = getattr(settings, 'MAX_AGE_OF_CONSENT', 65)


def MinConsentAge(dob):
    rdelta = relativedelta(date.today(), dob)
    if rdelta.years < min_age_of_consent:
        raise ValidationError(
            'Participant must be {} yrs or older. Got {} using DOB=\'{}\'.'.format(
                min_age_of_consent, rdelta.years, dob))


def MaxConsentAge(dob):
    rdelta = relativedelta(date.today(), dob)
    if rdelta.years > max_age_of_consent:
        raise ValidationError(
            'Participant must be younger than {} yrs. Got {} using DOB=\'{}\'.'.format(
                max_age_of_consent, rdelta.years, dob))
