import uuid

from django.db.models.fields import UUIDField

from .base_model import BaseModel


class BaseUuidModel(BaseModel):

    """Base model class for all models using an UUID and not an INT for the primary key. """

    id = UUIDField(
        blank=True,
        default=uuid.uuid4,
        editable=False,
        help_text="System auto field. UUID primary key.",
        primary_key=True,
    )

    class Meta:
        abstract = True
