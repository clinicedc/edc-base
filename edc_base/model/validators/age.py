from datetime import date
from dateutil.relativedelta import relativedelta

from django.core.exceptions import ValidationError

from edc.core.bhp_variables.models import StudySpecific


def MinConsentAge(value):
    try:
        ss = StudySpecific.objects.all()[0]
    except IndexError as e:
        raise IndexError(u'{0}. Have you filled in the required information in bhp_variables.StudySpecific?'.format(e))

    min_consent_age_years = ss.minimum_age_of_consent
    rdelta = relativedelta(date.today(), value)
    if rdelta.years < min_consent_age_years:
        raise ValidationError(u'Participant must be {0}yrs or older. Date of birth suggests otherwise. You entered {1} that suggests that the person is {2}yrs'.format(min_consent_age_years, value, rdelta.years))


def MaxConsentAge(value):
    try:
        ss = StudySpecific.objects.all()[0]
    except IndexError as e:
        raise IndexError(u'{0}. Have you filled in the required information in bhp_variables.StudySpecific?'.format(e))

    max_consent_age_years = ss.maximum_age_of_consent
    rdelta = relativedelta(date.today(), value)
    if rdelta.years > max_consent_age_years:
        raise ValidationError(u'Participant must be no older than {0}yrs. Date of birth suggests otherwise. You entered {1} that suggests that the person is {2}yrs'.format(max_consent_age_years, value, rdelta.years))
