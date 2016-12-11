from model_mommy import mommy

from django.apps import apps as django_apps

from edc_base.utils import get_utcnow
from edc_base.exceptions import FutureDateError
from edc_visit_tracking.constants import SCHEDULED
from edc_metadata.models import CrfMetadata
from edc_metadata.constants import REQUIRED


class TestMixinError(Exception):
    pass


class ReferenceDateMixin:
    """Sets the reference date to the earliest consent date."""
    def setUp(self):
        app_config = django_apps.get_app_config('edc_consent')
        self.mixin_reference_datetime = app_config.testconsentstart
        super(ReferenceDateMixin, self).setUp()


class AddVisitMixin:

    def add_visit(self, model_label, visit_code, reason=None):
        """Adds (or gets) and returns a visit for give model and code."""
        Appointment = django_apps.get_app_config('edc_appointment').model
        reason = reason or SCHEDULED
        model = django_apps.get_model(*model_label.split('.'))
        try:
            appointment = Appointment.objects.get(
                subject_identifier=self.subject_identifier, visit_code=visit_code)
            if appointment.appt_datetime > get_utcnow():
                raise FutureDateError(
                    'For testing, create visits without future dates. Got {}, {}'.format(
                        appointment.visit_code,
                        appointment.appt_datetime))
            try:
                visit = self.get_visit(model_label, visit_code)
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

    def add_visits(self, model_label, *codes):
        """Adds a sequence of visits for the codes provided.

        If a infant visit already exists, it will just pass."""
        for code in codes:
            self.add_visit(model_label, code)

    def get_visit(self, model_label, code):
        """Returns a visit instance if it exists."""
        model = django_apps.get_model(*model_label.split('.'))
        visit = model.objects.get(
            appointment__subject_identifier=self.subject_identifier, visit_code=code)
        return visit

    def get_last_visit(self, model_label):
        """Returns the last visit instance if it exists."""
        model = django_apps.get_model(*model_label.split('.'))
        return model.objects.filter(
            appointment__subject_identifier=self.subject_identifier).order_by('report_datetime').last()


class CompleteCrfsMixin:

    def mommy_options(self, report_datetime):
        """Override the default recipe options for your mommy recipe {label_lower: {key: value}, ...}."""
        return {}

    def get_crfs(self, visit_code):
        """Return a queryset of crf metadata for the visit."""
        return CrfMetadata.objects.filter(
            subject_identifier=self.subject_identifier,
            visit_code=visit_code).order_by('show_order')

    def get_required_crfs(self, visit_code):
        """Return a queryset of REQUIRED crf metadata for the visit."""
        return self.get_crfs(visit_code).filter(entry_status=REQUIRED).order_by('show_order')

    def complete_required_crfs(self, visit_code, visit, visit_attr):
        """Complete all CRFs in a visit by looping through metadata.

        Revisit the metadata on each loop as rule_groups may change the entry status of CRFs."""
        completed_crfs = []
        while True:
            for crf in self.get_required_crfs(visit_code):
                options = self.mommy_options(visit.report_datetime).get(crf.model, {})
                options.update({
                    visit_attr: visit,
                    'report_datetime': visit.report_datetime})
                completed_crfs.append(
                    mommy.make_recipe(crf.model, **options))
            if not self.get_required_crfs(visit_code):
                break
        return completed_crfs
