from ..fields import UUIDAutoField

from .base_model import BaseModel


class BaseUuidModel(BaseModel):

    """Base model class for all models using an UUID and not an INT for the primary key. """

    id = UUIDAutoField(
        primary_key=True,
        editable=False,
        help_text="System field. UUID primary key.")

    class Meta:
        abstract = True
