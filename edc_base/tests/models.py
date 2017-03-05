from django.db import models

from edc_base.model_mixins import BaseUuidModel
from edc_base.model_validators import CompareNumbersValidator


class TestModel(BaseUuidModel):

    f1 = models.CharField(max_length=10)
    f2 = models.CharField(max_length=10)
    f3 = models.CharField(max_length=10, null=True, blank=False)
    f4 = models.CharField(max_length=10, null=True, blank=False)
    f5 = models.CharField(max_length=10)


class TestValidatorModel(models.Model):

    consent_age = models.IntegerField(
        validators=[
            CompareNumbersValidator(
                18, '>=', message='Age of consent must be {}. Got {}'),
            CompareNumbersValidator(
                64, '<=', message='Age of consent must be {}. Got {}')
        ])
