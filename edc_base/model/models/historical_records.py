from uuid import uuid4

from simple_history.models import HistoricalRecords as SimpleHistoricalRecords

from django.db.models import UUIDField

from django.apps import apps

try:
    from edc_sync.mixins import SyncMixin
except ImportError:
    pass


class HistoricalRecords(SimpleHistoricalRecords):

    def get_extra_fields(self, model, fields):
        fields = super(HistoricalRecords, self).get_extra_fields(model, fields)
        fields['history_id'] = UUIDField(primary_key=True, default=uuid4)
        return fields

    def add_extra_methods(self, cls):
        super(HistoricalRecords, self).add_extra_methods(cls)
        try:
            apps.get_app_config('edc_sync')
            for key, func in SyncMixin.__dict__.items():
                if not key.startswith('__'):
                    setattr(cls, key, func)
        except (LookupError, NameError):
            pass
