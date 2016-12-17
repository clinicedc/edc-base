import socket

from django.db import models
from django_revision import RevisionField

from ...utils import get_utcnow

from ..constants import BASE_MODEL_UPDATE_FIELDS
from ..fields import HostnameModificationField, UserField


class BaseModel(models.Model):

    """Base model class for all models. Adds created and modified'
    values for user, date and hostname (computer)."""

    get_latest_by = 'modified'

    created = models.DateTimeField(
        default=get_utcnow,
        editable=False)

    modified = models.DateTimeField(
        default=get_utcnow,
        editable=False)

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
        self.common_clean()
        try:
            # don't allow update_fields to bypass these audit fields
            update_fields = kwargs.get('update_fields', None) + BASE_MODEL_UPDATE_FIELDS
            kwargs.update({'update_fields': update_fields})
        except TypeError:
            pass
        super(BaseModel, self).save(*args, **kwargs)

    def common_clean(self, cleaned_data=None):
        """A method that can be shared between form clean and model.save."""
        pass

    @property
    def verbose_name(self):
        return self._meta.verbose_name

    class Meta:
        get_latest_by = 'modified'
        ordering = ('-modified', '-created',)
        abstract = True
