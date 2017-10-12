import sys

from django.db import models
from django.db.models.deletion import PROTECT
from django.contrib.auth.models import User


class UserProfile(models.Model):

    user = models.OneToOneField(User, on_delete=PROTECT)

    study_site = models.CharField(
        max_length=100,
        blank=True,
        null=True)

    study_country = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        help_text='user\'s country of work')

    country = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        help_text='user\'s country of origin')


if 'test' in sys.argv:
    from .tests.models import TestModel, TestValidatorModel
