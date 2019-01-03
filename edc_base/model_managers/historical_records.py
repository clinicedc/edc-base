import uuid

from django.db import models
from django.utils.timezone import now
from simple_history.models import HistoricalRecords as SimpleHistoricalRecords
from simple_history.signals import pre_create_historical_record
from simple_history.signals import post_create_historical_record


class SerializableModelManager(models.Manager):

    def get_by_natural_key(self, history_id):
        return self.get(history_id=history_id)


class SerializableModel(models.Model):

    objects = SerializableModelManager()

    def natural_key(self):
        return (self.history_id, )

    class Meta:
        abstract = True


class HistoricalRecords(SimpleHistoricalRecords):

    """HistoricalRecords that forces a UUID primary key,
    has a natural key method available for serialization,
    and respects \'using\'.
    """

    model_cls = SerializableModel

    def __init__(self, **kwargs):
        """Defaults use of UUIDField instead of AutoField and
        serializable base.
        """
        kwargs.update(bases=(self.model_cls, ))
        kwargs.update(history_id_field=models.UUIDField(default=uuid.uuid4))
        super().__init__(**kwargs)

    def post_save(self, instance, created, using=None, **kwargs):
        if not created and hasattr(instance, "skip_history_when_saving"):
            return
        if not kwargs.get("raw", False):
            self.create_historical_record(instance, created and "+" or "~", using=using)

    def post_delete(self, instance, using=None, **kwargs):
        if self.cascade_delete_history:
            manager = getattr(instance, self.manager_name)
            manager.using(using).all().delete()
        else:
            self.create_historical_record(instance, "-", using=using)

    def create_historical_record(self, instance, history_type, using=None):
        history_date = getattr(instance, "_history_date", now())
        history_user = self.get_history_user(instance)
        history_change_reason = getattr(instance, "changeReason", None)
        manager = getattr(instance, self.manager_name)

        attrs = {}
        for field in self.fields_included(instance):
            attrs[field.attname] = getattr(instance, field.attname)

        history_instance = manager.model(
            history_date=history_date,
            history_type=history_type,
            history_user=history_user,
            history_change_reason=history_change_reason,
            **attrs
        )

        pre_create_historical_record.send(
            sender=manager.model,
            instance=instance,
            history_date=history_date,
            history_user=history_user,
            history_change_reason=history_change_reason,
            history_instance=history_instance,
        )

        history_instance.save(using=using)

        post_create_historical_record.send(
            sender=manager.model,
            instance=instance,
            history_instance=history_instance,
            history_date=history_date,
            history_user=history_user,
            history_change_reason=history_change_reason,
        )
