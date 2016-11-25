import string

from datetime import date
from dateutil.relativedelta import relativedelta
from faker import Faker
from faker.providers import BaseProvider
from model_mommy.recipe import Recipe, seq
from random import choice

from django.apps import apps as django_apps


class EdcProvider(BaseProvider):

    def initials(self):
        return choice(list(string.ascii_uppercase)) + choice(list(string.ascii_uppercase))

    def dob_for_consenting_adult(self):
        consent_config = django_apps.get_app_config(
            'edc_consent').get_consent_config('edc_example.subjectconsent')
        years = choice(range(consent_config.age_is_adult, consent_config.age_max))
        return date.today() - relativedelta(years=years)

    def dob_for_consenting_minor(self):
        consent_config = django_apps.get_app_config(
            'edc_consent').get_consent_config('edc_example.subjectconsent')
        years = choice(range(consent_config.age_min, consent_config.age_is_adult) - 1)
        return date.today() - relativedelta(years=years)


edc_faker = Faker()
edc_faker.add_provider(EdcProvider)
