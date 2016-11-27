import string

from datetime import date
from dateutil.relativedelta import relativedelta
from faker.providers import BaseProvider
from model_mommy.recipe import Recipe, seq
from random import choice

from django.apps import apps as django_apps
from django.utils import timezone


class EdcBaseProvider(BaseProvider):

    consent_model = 'edc_example.subjectconsent'

    def initials(self):
        return choice(list(string.ascii_uppercase)) + choice(list(string.ascii_uppercase))

    def dob_for_consenting_adult(self):
        consent_config = django_apps.get_app_config(
            'edc_consent').get_consent_config(self.consent_model)
        years = choice(range(consent_config.age_is_adult, consent_config.age_max))
        return timezone.now() - relativedelta(years=years)

    def dob_for_consenting_minor(self):
        consent_config = django_apps.get_app_config(
            'edc_consent').get_consent_config(self.consent_model)
        years = choice(range(consent_config.age_min, consent_config.age_is_adult) - 1)
        return timezone.now() - relativedelta(years=years)

    def yesterday(self):
        return timezone.now() - relativedelta(days=1)

    def last_week(self):
        return timezone.now() - relativedelta(weeks=1)

    def last_month(self):
        return timezone.now() - relativedelta(months=1)

    def two_months_ago(self):
        return timezone.now() - relativedelta(months=2)

    def three_months_ago(self):
        return timezone.now() - relativedelta(months=3)

    def six_months_ago(self):
        return timezone.now() - relativedelta(months=6)

    def twelve_months_ago(self):
        return timezone.now() - relativedelta(months=12)
