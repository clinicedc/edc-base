from django.apps import AppConfig as DjangoAppConfig


class AppConfig(DjangoAppConfig):
    name = 'edc_base_test'
    consent_model = 'edc_example.subjectconsent'
    survey_group_name = 'example_survey'
