from simple_history.models import HistoricalRecords as SimpleHistoricalRecords

from django.db import models
from django.db.models.fields import AutoField

from ..utils import get_utcnow


class SerializableManager(models.Manager):

    def get_by_natural_key(self, history_id):
        return self.get(history_id=history_id)


class SerializableModel(models.Model):

    objects = SerializableManager()

    def natural_key(self):
        return self.history_id

    class Meta:
        abstract = True


class HistoricalRecords(SimpleHistoricalRecords):

    """HistoricalRecords that uses a UUID primary key and has a natural key method."""

    def __init__(self, verbose_name=None, bases=(models.Model,),
                 user_related_name='+', table_name=None, inherit=False):
        bases = (SerializableModel, )
        super(HistoricalRecords, self).__init__(
            verbose_name=verbose_name, bases=bases, user_related_name=user_related_name,
            table_name=table_name, inherit=inherit)

    def get_history_id_field(self, model):
        """Return a field instance without initially assuming
        it should be AutoField.

        For example, primary key is UUIDField(primary_key=True, default=uuid.uuid4)"""
        try:
            field = [
                field for field in model._meta.fields if field.primary_key][0]
            field = field.__class__(primary_key=True, default=field.default)
        except (IndexError, TypeError):
            field = AutoField(primary_key=True)
        return field

    def get_extra_fields(self, model, fields):
        """Override to set history_id (to UUIDField)."""
        extra_fields = super(
            HistoricalRecords, self).get_extra_fields(model, fields)
        extra_fields.update({'history_id': self.get_history_id_field(model)})
        extra_fields.update({'natural_key': lambda x: x.history_id})
        return extra_fields

    def post_save(self, instance, created, **kwargs):
        """Override to include \'using\'."""
        if not created and hasattr(instance, 'skip_history_when_saving'):
            return
        if not kwargs.get('raw', False):
            self.create_historical_record(
                instance, created and '+' or '~', using=kwargs.get('using'))

    def post_delete(self, instance, **kwargs):
        """Override to include \'using\'."""
        self.create_historical_record(instance, '-', using=kwargs.get('using'))

    def create_historical_record(self, instance, history_type, **kwargs):
        """Override to include \'using\'."""
        history_date = getattr(instance, '_history_date', get_utcnow())
        history_user = self.get_history_user(instance)
        manager = getattr(instance, self.manager_name)
        attrs = {}
        for field in instance._meta.fields:
            attrs[field.attname] = getattr(instance, field.attname)
        manager.using(kwargs.get('using')).create(history_date=history_date, history_type=history_type,
                                                  history_user=history_user, **attrs)
