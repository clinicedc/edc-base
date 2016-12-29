import sys

from dateutil.relativedelta import relativedelta

from django.apps import apps as django_apps
from django.core.management.color import color_style

from edc_consent.site_consents import site_consents
from datetime import timedelta


class DatesTestMixin:

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        style = color_style()
        sys.stdout.write(
            style.NOTICE(
                '\nNOTICE. Overwriting study open/close and consent.start/end dates for tests only. '
                'See {}\n'.format(cls.__name__)))
        study_open_datetime = django_apps.app_configs['edc_protocol'].study_open_datetime
        study_close_datetime = django_apps.app_configs['edc_protocol'].study_close_datetime
        duration_delta = relativedelta(study_close_datetime, study_open_datetime)
        django_apps.app_configs['edc_protocol'].study_open_datetime = study_open_datetime - duration_delta
        django_apps.app_configs['edc_protocol'].study_close_datetime = study_open_datetime

        edc_protocol_app_config = django_apps.get_app_config('edc_protocol')
        study_open_datetime = edc_protocol_app_config.study_open_datetime
        study_close_datetime = edc_protocol_app_config.study_close_datetime
        sys.stdout.write(style.NOTICE(' * new study open datetime: {}\n'.format(study_open_datetime)))
        sys.stdout.write(style.NOTICE(' * new study close datetime: {}\n'.format(study_close_datetime)))
        testconsents = []
        for consent in site_consents.registry:
            tdelta = consent.start - study_open_datetime
            consent_period_tdelta = consent.end - consent.start
            consent.start = consent.start - tdelta
            consent.end = consent.start + consent_period_tdelta - timedelta(minutes=24 * 60)
            sys.stdout.write(style.NOTICE(' * {}: {} - {}\n'.format(consent.model_name, consent.start, consent.end)))
            testconsents.append(consent)
        site_consents.reset_registry()
        for consent in testconsents:
            site_consents.register(consent)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        site_consents.reset_registry()
        site_consents.autodiscover(verbose=False)

    def get_utcnow(self):
        return self.study_open_datetime

    @property
    def study_open_datetime(self):
        edc_protocol_app_config = django_apps.get_app_config('edc_protocol')
        return edc_protocol_app_config.study_open_datetime

    @property
    def study_close_datetime(self):
        edc_protocol_app_config = django_apps.get_app_config('edc_protocol')
        return edc_protocol_app_config.study_close_datetime
