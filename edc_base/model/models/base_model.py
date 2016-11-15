import socket

from django.db import models
from django_extensions.db.models import TimeStampedModel
from django_revision import RevisionField

from ..constants import BASE_MODEL_UPDATE_FIELDS
from ..fields import HostnameModificationField, UserField


class BaseModel(TimeStampedModel):

    """Base model class for all models. Adds created and modified'
    values for user, date and hostname (computer)."""

    get_latest_by = 'modified'

    user_created = UserField(
        max_length=50,
        verbose_name='user created',
        editable=False,
    )

    user_modified = UserField(
        max_length=50,
        verbose_name='user modified',
        editable=False,
    )

    hostname_created = models.CharField(
        max_length=50,
        editable=False,
        default=socket.gethostname(),
        help_text="System field. (modified on create only)",
    )

    hostname_modified = HostnameModificationField(
        max_length=50,
        editable=False,
        help_text="System field. (modified on every save)",
    )

    revision = RevisionField(
        help_text="System field. Git repository tag:branch:commit."
    )

    objects = models.Manager()

    def save(self, *args, **kwargs):
        try:
            # don't allow update_fields to bypass these audit fields
            update_fields = kwargs.get('update_fields', None) + BASE_MODEL_UPDATE_FIELDS
            kwargs.update({'update_fields': update_fields})
        except TypeError:
            pass
        super(BaseModel, self).save(*args, **kwargs)

    class Meta:
        abstract = True
