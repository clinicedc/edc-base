import os

from django.apps import AppConfig as DjangoAppConfig
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


class AppConfig(DjangoAppConfig):
    name = 'edc_base'
    institution = 'My Institution'
    project_name = 'My Project Title'
    config_folder = os.path.join(settings.BASE_DIR.ancestor(1), 'etc')

    def ready(self):
        if not os.path.exists(self.config_folder):
            raise ImproperlyConfigured('Missing configuration folder {}. '
                                       'Please create'.format(self.config_folder))
