from django.core.exceptions import ValidationError

from edc.core.bhp_variables.models import StudySpecific
from edc.core.bhp_variables.choices import GENDER_OF_CONSENT


def GenderOfConsent(value):
    ss = StudySpecific.objects.all()[0]

    gender_allowed = ss.gender_of_consent

    if gender_allowed == 'MF':
        allowed = ('MF', 'Male and Female')
        entry = ('value', value)
    else:
        for lst in GENDER_OF_CONSENT:
            if lst[0] == gender_allowed:
                allowed = lst

        for lst in GENDER_OF_CONSENT:
            if lst[0] == value:
                entry = lst

    if value != allowed[0] and allowed[0] != 'MF':
        raise ValidationError(u'Gender of consent is %s. You entered %s.' % (allowed[1], entry[1]))
