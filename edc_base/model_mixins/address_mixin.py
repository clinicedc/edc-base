from django.db import models


class AddressMixin(models.Model):

    address = models.CharField(
        verbose_name='Address',
        null=True,
        blank=True,
        max_length=50)

    postal_code = models.CharField(
        null=True,
        blank=True,
        max_length=50)

    city = models.CharField(
        null=True,
        blank=True,
        max_length=50)

    country = models.CharField(
        null=True,
        blank=True,
        max_length=50)

    telephone = models.CharField(
        null=True,
        blank=True,
        max_length=50)

    mobile = models.CharField(
        null=True,
        blank=True,
        max_length=50)

    fax = models.CharField(
        null=True,
        blank=True,
        max_length=50)

    email = models.EmailField(
        null=True,
        blank=True,
        max_length=50)

    class Meta:
        abstract = True
