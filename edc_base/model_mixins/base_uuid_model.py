from ..model_fields import UUIDAutoField

from .base_model import BaseModel


class BaseUuidModel(BaseModel):

    """Base model class for all models using an UUID and not
    an INT for the primary key.
    """

    id = UUIDAutoField(
        blank=True,
        editable=False,
        help_text="System auto field. UUID primary key.",
        primary_key=True)

    class Meta:
        abstract = True
