from django.db import models

from simple_history.models import HistoricalRecords

from edc_base.model.models import BaseUuidModel
from edc_base.model.validators.compare_numbers import CompareNumbersValidator


class TestModel(BaseUuidModel):

    f1 = models.CharField(max_length=10)
    f2 = models.CharField(max_length=10)
    f3 = models.CharField(max_length=10, null=True, blank=False)
    f4 = models.CharField(max_length=10, null=True, blank=False)
    f5 = models.CharField(max_length=10)

    history = HistoricalRecords()

    class Meta:
        app_label = 'edc_base_example'


class TestValidatorModel(models.Model):

    consent_age = models.IntegerField(
        validators=[
            CompareNumbersValidator(18, '>=', message='Age of consent must be {}. Got {}'),
            CompareNumbersValidator(64, '<=', message='Age of consent must be {}. Got {}')
        ])

    class Meta:
        app_label = 'edc_base_example'
