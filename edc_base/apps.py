import sys

from django.apps import AppConfig as DjangoAppConfig
from django.conf import settings
from django.db.backends.signals import connection_created
from django.core.management.color import color_style

style = color_style()


def activate_foreign_keys(sender, connection, **kwargs):
    """Enable integrity constraint with sqlite."""
    if connection.vendor == 'sqlite':
        cursor = connection.cursor()
        cursor.execute('PRAGMA foreign_keys = ON;')


class AppConfig(DjangoAppConfig):
    name = 'edc_base'
    institution = 'My Institution'
    project_name = 'My Project Title'

    def ready(self):
        sys.stdout.write('Loading {} ...\n'.format(self.verbose_name))
        connection_created.connect(activate_foreign_keys)
        tzname = settings.TIME_ZONE
        sys.stdout.write(' * TIME ZONE {}.\n'.format(settings.TIME_ZONE))
        if tzname != 'UTC':
            sys.stdout.write(style.WARNING(' * Warning: timezone is not UTC!\n'))
        sys.stdout.write(' Done loading {}.\n'.format(self.verbose_name))
