from simple_history.models import HistoricalRecords as SimpleHistoricalRecords

from django.db.models.fields import AutoField
from django.utils.timezone import now

# try:
#     from edc_sync.mixins import SyncMixin
# except ImportError:
#     pass
#
#
# class HistoricalRecords(SimpleHistoricalRecords):
#
#     def get_extra_fields(self, model, fields):
#         fields = super(HistoricalRecords, self).get_extra_fields(model, fields)
#         fields['history_id'] = UUIDField(primary_key=True, default=uuid4)
#         return fields
#
#     def add_extra_methods(self, cls):
#         super(HistoricalRecords, self).add_extra_methods(cls)
#         try:
#             apps.get_app_config('edc_sync')
#             for key, func in SyncMixin.__dict__.items():
#                 if not key.startswith('__'):
#                     setattr(cls, key, func)
#         except (LookupError, NameError):
#             pass


class HistoricalRecords(SimpleHistoricalRecords):

    """HistoricalRecords that uses a UUID primary key and has a natural key method."""

    def get_history_id_field(self, model):
        """Return a field instance without initially assuming
        it should be AutoField.

        For example, primary key is UUIDField(primary_key=True, default=uuid.uuid4)"""
        try:
            field = [field for field in model._meta.fields if field.primary_key][0]
            field = field.__class__(primary_key=True, default=field.default)
        except (IndexError, TypeError):
            field = AutoField(primary_key=True)
        return field

    def get_extra_fields(self, model, fields):
        """Override to set history_id (to UUIDField) and add the
        SyncModelMixin methods."""
        extra_fields = super(HistoricalRecords, self).get_extra_fields(model, fields)
        extra_fields.update({'history_id': self.get_history_id_field(model)})
        return extra_fields

    def post_save(self, instance, created, **kwargs):
        """Override to include \'using\'."""
        if not created and hasattr(instance, 'skip_history_when_saving'):
            return
        if not kwargs.get('raw', False):
            self.create_historical_record(instance, created and '+' or '~', using=kwargs.get('using'))

    def post_delete(self, instance, **kwargs):
        """Override to include \'using\'."""
        self.create_historical_record(instance, '-', using=kwargs.get('using'))

    def create_historical_record(self, instance, history_type, **kwargs):
        """Override to include \'using\'."""
        history_date = getattr(instance, '_history_date', now())
        history_user = self.get_history_user(instance)
        manager = getattr(instance, self.manager_name)
        attrs = {}
        for field in instance._meta.fields:
            attrs[field.attname] = getattr(instance, field.attname)
        manager.using(kwargs.get('using')).create(history_date=history_date, history_type=history_type,
                                                  history_user=history_user, **attrs)
