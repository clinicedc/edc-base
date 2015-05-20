import uuid

from django.db import models
from revision import RevisionField

from ..constants import BASE_UUID_MODEL_UPDATE_FIELDS

from .base_model import BaseModel


class BaseUuidModel(BaseModel):

    """Base model class for all models using an UUID and not an INT for the primary key. """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        help_text="System field. UUID primary key.")

    revision = RevisionField(
        help_text="System field. Git repository tag:branch:commit."
    )

    def save(self, *args, **kwargs):
        try:
            update_fields = kwargs.get('update_fields', None) + BASE_UUID_MODEL_UPDATE_FIELDS
            kwargs.update({'update_fields': update_fields})
        except TypeError:
            pass
        super(BaseUuidModel, self).save(*args, **kwargs)

    class Meta:
        abstract = True
