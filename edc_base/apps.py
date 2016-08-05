from django.apps import AppConfig as DjangoAppConfig


class AppConfig(DjangoAppConfig):
    name = 'edc_base'
    institution = 'My Institution'
    verbose_name = 'My Project Title'
