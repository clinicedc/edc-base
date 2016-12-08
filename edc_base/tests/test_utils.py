from datetime import datetime, date

from django.test.testcases import TestCase
from edc_base.utils import age
import pytz


class TestEdcBase(TestCase):

    def test_age(self):
        born = date(1990, 5, 1)
        reference_datetime = pytz.utc.localize(datetime(2000, 5, 1))
        self.assertEqual(age(born, reference_datetime).years, 10)

    def test_age_without_tz(self):
        born = date(1990, 5, 1)
        reference_datetime = datetime(2000, 5, 1)
        self.assertRaises(ValueError, age, born, reference_datetime)
