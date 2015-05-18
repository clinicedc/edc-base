from django.core.urlresolvers import reverse
from django.db import models
from django_extensions.db.models import TimeStampedModel

from ..constants import BASE_MODEL_UPDATE_FIELDS
from ..fields import HostnameCreationField, HostnameModificationField


class BaseModel(TimeStampedModel):

    """Base model class for all models. Adds created and modified'
    values for user, date and hostname (computer).


    Note: ANY additional fields """

    user_created = models.CharField(
        max_length=250,
        verbose_name='user created',
        editable=False,
        default="",
        db_index=True,
        help_text="system field."
    )

    user_modified = models.CharField(
        max_length=250,
        verbose_name='user modified',
        editable=False,
        default="",
        db_index=True,
        help_text="system field.",
    )

    hostname_created = HostnameCreationField(
        db_index=True,
        help_text="system field.",
    )

    hostname_modified = HostnameModificationField(
        db_index=True,
        help_text="system field.",
    )

    def save(self, *args, **kwargs):
        try:
            # don't allow update_fields to bypass these audit fields
            update_fields = kwargs.get('update_fields', None) + BASE_MODEL_UPDATE_FIELDS
            kwargs.update({'update_fields': update_fields})
        except TypeError:
            pass
        super(BaseModel, self).save(*args, **kwargs)

    def get_absolute_url(self):
        if self.id:
            url = reverse('admin:{app_label}_{object_name}_change'.format(app_label=self._meta.app_label, object_name=self._meta.object_name.lower()), args=(self.id,))
        else:
            url = reverse('admin:{app_label}_{object_name}_add'.format(app_label=self._meta.app_label, object_name=self._meta.object_name.lower()))
        return url

    @classmethod
    def encrypted_fields(self):
        from edc.core.crypto_fields.fields import BaseEncryptedField
        return [fld.name for fld in self._meta.fields if isinstance(fld, BaseEncryptedField)]

    class Meta:
        abstract = True
