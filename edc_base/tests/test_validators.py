from datetime import date
from django import forms
from django.db import models
from django.test import TestCase
from edc_base.model.validators import (
    MaxConsentAgeValidator, GenderOfConsent, CompareNumbersValidator, MinConsentAgeValidator)
from dateutil.relativedelta import relativedelta
from django.core.exceptions import ValidationError, ImproperlyConfigured


class TestValidatorModel(models.Model):

    consent_age = models.IntegerField(
        validators=[
            CompareNumbersValidator(18, '>=', message='Age of consent must be {}. Got {}'),
            CompareNumbersValidator(64, '<=', message='Age of consent must be {}. Got {}')
        ])

    class Meta:
        app_label = 'edc_base'


class TestValidationForm(forms.ModelForm):

    class Meta:
        model = TestValidatorModel
        fields = '__all__'


class TestValidators(TestCase):

    def test_min_age_validator(self):
        validator = MinConsentAgeValidator(18)
        self.assertRaises(ValidationError, validator, date.today() - relativedelta(years=17))
        self.assertIsNone(validator(date.today() - relativedelta(years=18)))
        self.assertIsNone(validator(date.today() - relativedelta(years=19)))

    def test_max_age_validator(self):
        validator = MaxConsentAgeValidator(64)
        self.assertRaises(ValidationError, validator, date.today() - relativedelta(years=65))
        self.assertIsNone(validator(date.today() - relativedelta(years=64)))
        self.assertIsNone(validator(date.today() - relativedelta(years=63)))

    def test_gender_of_consent_none(self):
        with self.settings(GENDER_OF_CONSENT='MF'):
            value = None
            self.assertRaises(ValidationError, GenderOfConsent, value)

    def test_gender_of_consent_in(self):
        with self.settings(GENDER_OF_CONSENT='MF'):
            value = 'M'
            self.assertIsNone(GenderOfConsent(value))

    def test_gender_of_consent_as_list(self):
        with self.settings(GENDER_OF_CONSENT=['M', 'F']):
            value = 'M'
            self.assertIsNone(GenderOfConsent(value))

    def test_compare_numbers_gt(self):
            validator = CompareNumbersValidator(10, '>')
            self.assertRaises(ValidationError, validator, 9)
            self.assertRaises(ValidationError, validator, 10)
            self.assertIsNone(validator(11))

    def test_compare_numbers_gte(self):
            validator = CompareNumbersValidator(10, '>=')
            self.assertRaises(ValidationError, validator, 9)
            self.assertIsNone(validator(10))
            self.assertIsNone(validator(11))

    def test_compare_numbers_lt(self):
            validator = CompareNumbersValidator(10, '<')
            self.assertIsNone(validator(9))
            self.assertRaises(ValidationError, validator, 10)
            self.assertRaises(ValidationError, validator, 11)

    def test_compare_numbers_none2(self):
            self.assertRaises(TypeError, CompareNumbersValidator)

    def test_compare_numbers_no_value(self):
            self.assertRaises(ImproperlyConfigured, CompareNumbersValidator, None, '<')

    def test_compare_numbers_no_values(self):
            self.assertRaises(ImproperlyConfigured, CompareNumbersValidator, None, None)

    def test_compare_numbers_not_numbers(self):
            self.assertRaises(TypeError, CompareNumbersValidator([1, 2], '<'), 1)  # nonsense
            self.assertRaises(ValidationError, CompareNumbersValidator('ABC', '<'), 'ABCD')  # nonsense

    def test_age_of_consent(self):
        form = TestValidationForm(data={'consent_age': 17})
        self.assertFalse(form.is_valid())
        form = TestValidationForm(data={'consent_age': 18})
        self.assertTrue(form.is_valid())
        form = TestValidationForm(data={'consent_age': 64})
        self.assertTrue(form.is_valid())
        form = TestValidationForm(data={'consent_age': 65})
        self.assertFalse(form.is_valid())
