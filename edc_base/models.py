from django.db import models

from edc_base.model.models import BaseUuidModel, HistoricalRecords


class TestModel(BaseUuidModel):

    f1 = models.CharField(max_length=10)
    f2 = models.CharField(max_length=10)
    f3 = models.CharField(max_length=10, null=True, blank=False)
    f4 = models.CharField(max_length=10, null=True, blank=False)
    f5 = models.CharField(max_length=10)

    history = HistoricalRecords()

    class Meta:
        app_label = 'edc_base'
