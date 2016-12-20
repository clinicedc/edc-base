import pytz

from datetime import datetime, date

from django.test.testcases import TestCase

from edc_base.utils import age, get_age_in_days, formatted_age, get_safe_random_string


class TestUtils(TestCase):

    def test_get_safe_random_string(self):
        '''With default parameters'''
        _safe_string = get_safe_random_string()
        allowed_chars = 'ABCDEFGHKMNPRTUVWXYZ2346789'
        for character in _safe_string:
            if character not in allowed_chars:
                assert False

    def test_formatted_age(self):
        self.assertEqual(
            formatted_age(date(1990, 12, 12), pytz.utc.localize(datetime(2016, 12, 12))), '26y')
        self.assertEqual(
            formatted_age(date(2016, 9, 9), pytz.utc.localize(datetime(2016, 12, 12))), '3m')
        self.assertEqual(
            formatted_age(date(2016, 10, 28), pytz.utc.localize(datetime(2016, 12, 12))), '1m14d')
        self.assertEqual(
            formatted_age(date(2016, 12, 6), pytz.utc.localize(datetime(2016, 12, 12))), '6d')
        self.assertEqual(
            formatted_age(date(2015, 12, 12), pytz.utc.localize(datetime(2016, 12, 12))), '12m')

    def test_age_in_days(self):
        born = date(2016, 10, 20)
        reference_date = pytz.utc.localize(datetime(2016, 10, 28))
        self.assertEqual(get_age_in_days(reference_date, born), 8)

    def test_age(self):
        born = date(1990, 5, 1)
        reference_dt = pytz.utc.localize(datetime(2000, 5, 1))
        self.assertEqual(age(born, reference_dt).years, 10)

    def test_age_without_tz(self):
        born = pytz.utc.localize(datetime(1990, 5, 1))
        reference_dt = datetime(2000, 5, 1)
        self.assertEqual(age(born, reference_dt).years, 10)

    def test_age_born_date(self):
        born = date(1990, 5, 1)
        reference_dt = datetime(2000, 5, 1)
        self.assertEqual(age(born, reference_dt).years, 10)

    def test_age_reference_as_date(self):
        born = pytz.utc.localize(datetime(1990, 5, 1))
        reference_dt = date(2000, 5, 1)
        self.assertEqual(age(born, reference_dt).years, 10)

    def test_age_hour_old(self):
        born = datetime(2000, 5, 1, 12, 0)
        reference_dt = datetime(2000, 5, 1, 14, 1)
        self.assertEqual(age(born, reference_dt).hours, 2)

    def test_reference_precedes_dob(self):
        born = datetime(2000, 5, 1, 12, 0)
        reference_dt = datetime(1990, 5, 1, 12, 0)
        self.assertRaises(ValueError, age, born, reference_dt)
