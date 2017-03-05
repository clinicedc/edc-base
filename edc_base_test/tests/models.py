from django.db.models.deletion import PROTECT
from django.db import models

from edc_appointment.models import Appointment
from edc_base.model_mixins import BaseUuidModel
from edc_visit_schedule.model_mixins import VisitScheduleModelMixin


class SubjectVisit(VisitScheduleModelMixin, BaseUuidModel):

    appointment = models.OneToOneField(Appointment, on_delete=PROTECT)


class TestModel(BaseUuidModel):

    subject_visit = models.ForeignKey(SubjectVisit, on_delete=PROTECT)
