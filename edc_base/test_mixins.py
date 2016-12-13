from model_mommy import mommy

from django.apps import apps as django_apps

from edc_base.utils import get_utcnow
from edc_base.exceptions import FutureDateError
from edc_visit_tracking.constants import SCHEDULED
from edc_metadata.models import CrfMetadata
from edc_metadata.constants import REQUIRED, NOT_REQUIRED


class TestMixinError(Exception):
    pass


class ReferenceDateMixin:
    """Sets the reference date to the earliest consent date."""
    def setUp(self):
        app_config = django_apps.get_app_config('edc_consent')
        self.test_mixin_reference_datetime = app_config.testconsentstart
        super(ReferenceDateMixin, self).setUp()


class LoadListDataMixin:

    list_data = None

    def load_list_data(self, label_lower):
        objs = []
        model = django_apps.get_model(*label_lower.split('.'))
        for name in self.list_data.get(label_lower):
            objs.append(model(name=name, short_name=name))
        model.objects.bulk_create(objs)


class AddVisitMixin:

    def add_visit(self, model_label=None, visit_code=None, reason=None, subject_identifier=None):
        """Adds (or gets) and returns a visit for give model and code."""
        Appointment = django_apps.get_app_config('edc_appointment').model
        reason = reason or SCHEDULED
        model = django_apps.get_model(*model_label.split('.'))
        try:
            appointment = Appointment.objects.get(
                subject_identifier=subject_identifier, visit_code=visit_code)
            if appointment.appt_datetime > get_utcnow():
                raise FutureDateError(
                    'For testing, create visits without future dates. Got {}, {}'.format(
                        appointment.visit_code,
                        appointment.appt_datetime))
            try:
                visit = self.get_visit(
                    visit_code=visit_code, model_label=model_label, subject_identifier=subject_identifier)
            except model.DoesNotExist:
                # create visit for the first time
                visit = mommy.make_recipe(
                    model_label,
                    appointment=appointment,
                    report_datetime=appointment.appt_datetime,
                    reason=reason)
        except Appointment.DoesNotExist as e:
            raise TestMixinError(
                '{} {}, {}. Did you complete the enrollment form?'.format(str(e), model_label, visit_code))
        return visit

    def add_visits(self, *codes, model_label=None, subject_identifier=None, reason=None):
        """Adds a sequence of visits for the codes provided.

        If a infant visit already exists, it will just pass."""
        for code in codes:
            self.add_visit(model_label=model_label, visit_code=code, reason=reason,
                           subject_identifier=subject_identifier)

    def get_visit(self, visit_code=None, model_label=None, subject_identifier=None):
        """Returns a visit instance if it exists."""
        model = django_apps.get_model(*model_label.split('.'))
        visit = model.objects.get(
            appointment__subject_identifier=subject_identifier, visit_code=visit_code)
        return visit

    def get_last_visit(self, model_label=None, subject_identifier=None):
        """Returns the last visit instance if it exists."""
        model = django_apps.get_model(*model_label.split('.'))
        return model.objects.filter(
            appointment__subject_identifier=subject_identifier).order_by('report_datetime').last()


class CompleteCrfsMixin:

    def mommy_options(self, report_datetime):
        """Override the default recipe options for your mommy recipe {label_lower: {key: value}, ...}."""
        return {}

    def get_crfs(self, visit_code=None, subject_identifier=None):
        """Return a queryset of crf metadata for the visit."""
        return CrfMetadata.objects.filter(
            subject_identifier=subject_identifier,
            visit_code=visit_code).order_by('show_order')

    def get_crfs_by_entry_status(self, visit_code=None, entry_status=None, subject_identifier=None):
        """Return a queryset of crf metadata for the visit by entry_status."""
        return self.get_crfs(
            visit_code=visit_code, subject_identifier=subject_identifier).filter(
                entry_status__in=entry_status).order_by('show_order')

    def complete_crfs(self, visit_code=None, visit=None, visit_attr=None, entry_status=None, subject_identifier=None):
        """Complete all CRFs in a visit by looping through metadata.

        Revisit the metadata on each loop as rule_groups may change the entry status of CRFs."""
        entry_status = entry_status or [REQUIRED, NOT_REQUIRED]
        if not isinstance(entry_status, (list, tuple)):
            entry_status = [entry_status]
        completed_crfs = []
        while True:
            for crf in self.get_crfs_by_entry_status(
                    visit_code=visit_code,
                    entry_status=entry_status,
                    subject_identifier=subject_identifier):
                options = self.mommy_options(visit.report_datetime).get(crf.model, {})
                options.update({
                    visit_attr: visit,
                    'report_datetime': visit.report_datetime})
                completed_crfs.append(
                    mommy.make_recipe(crf.model, **options))
            if not self.get_crfs_by_entry_status(
                    visit_code=visit_code, entry_status=entry_status, subject_identifier=subject_identifier):
                break
        return completed_crfs

    def complete_required_crfs(self, visit_code=None, visit=None, visit_attr=None, subject_identifier=None):
        return self.complete_crfs(
            visit_code=visit_code,
            visit=visit,
            visit_attr=visit_attr,
            entry_status=REQUIRED,
            subject_identifier=subject_identifier)
