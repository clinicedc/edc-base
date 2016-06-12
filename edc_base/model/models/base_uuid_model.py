import uuid

from .base_model import BaseModel
from django.db.models.fields import UUIDField


class BaseUuidModel(BaseModel):

    """Base model class for all models using an UUID and not an INT for the primary key. """

#     id = UUIDAutoField(
#         primary_key=True,
#         editable=False)

    id = UUIDField(
        blank=True,
        default=uuid.uuid4,
        editable=False,
        help_text="System auto field. UUID primary key.",
        primary_key=True,
    )

    class Meta:
        abstract = True
