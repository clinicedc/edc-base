import sys

from django.apps import AppConfig as DjangoAppConfig
from django.conf import settings
from django.db.backends.signals import connection_created
from django.core.management.color import color_style
from django.core.exceptions import ImproperlyConfigured

from .address import Address
from .utils import get_utcnow
from edc_base.site_list_data import site_list_data

style = color_style()


def activate_foreign_keys(sender, connection, **kwargs):
    """Enable integrity constraint with sqlite."""
    if connection.vendor == 'sqlite':
        cursor = connection.cursor()
        cursor.execute('PRAGMA foreign_keys = ON;')


class AppConfig(DjangoAppConfig):
    name = 'edc_base'
    institution = 'Institution (see edc_base.AppConfig.institution)'
    project_name = 'Project Title (see edc_base.AppConfig.project_name)'
    physical_address = Address()
    postal_address = Address()
    copyright = get_utcnow().year
    license = None
    disclaimer = 'For research purposes only.'
    default_url_name = 'home_url'

    def ready(self):
        from .signals import update_user_profile_on_post_save

        sys.stdout.write(f'Loading {self.verbose_name} ...\n')
        connection_created.connect(activate_foreign_keys)
        sys.stdout.write(
            f' * default TIME_ZONE {settings.TIME_ZONE}.\n')
        if not settings.USE_TZ:
            raise ImproperlyConfigured('EDC requires settings.USE_TZ = True')
        site_list_data.autodiscover()
        sys.stdout.write(f' Done loading {self.verbose_name}.\n')
