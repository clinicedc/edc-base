from ..constants import BASE_UUID_MODEL_UPDATE_FIELDS
from ..fields import UUIDAutoField, RevisionField

from .base_model import BaseModel


class BaseUuidModel(BaseModel):

    """Base model class for all models using an UUID and not an INT for the primary key. """

    id = UUIDAutoField(
        primary_key=True,
        help_text="system field. uuid primary key."
    )

    revision = RevisionField(
        help_text="system field. Git repository branch:commit."
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
