from dateutil.relativedelta import relativedelta
from django.test import TestCase

from model_mommy import mommy

from edc_base.utils import get_utcnow
from edc_base_test.mixins.add_visit_mixin import AddVisitMixin
from edc_visit_tracking.constants import SCHEDULED

from .models import TestModel, SubjectVisit
from edc_appointment.models import Appointment


class TestAll(TestCase):

    def test_add_visit(self):
        subject_identifier = '111111111'
        mixin_obj = AddVisitMixin()
        mommy.make_recipe('edc_registration.registeredsubject', subject_identifier=subject_identifier)
        for i in range(0, 3):
            mommy.make_recipe(
                'edc_appointment.appointment',
                subject_identifier=subject_identifier,
                timepoint=i,
                timepoint_datetime=get_utcnow() + relativedelta(months=i),
                visit_code='100' + str(i))
        visit_codes = [obj.visit_code for obj in Appointment.objects.filter(subject_identifier=subject_identifier)]
        mixin_obj.add_visit(
            SubjectVisit._meta.label_lower,
            visit_code=visit_codes[0],
            reason=SCHEDULED,
            subject_identifier=subject_identifier)
