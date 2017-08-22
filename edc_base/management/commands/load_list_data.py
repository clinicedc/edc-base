import sys

from django.apps import apps as django_apps
from django.core.management.base import BaseCommand, CommandError
from django.utils.module_loading import module_has_submodule
from importlib import import_module


class Command(BaseCommand):

    help = 'Populates the reference model'
    module_name = 'list_data'

    def add_arguments(self, parser):

        parser.add_argument(
            '--app_label',
            dest='app_label',
            default=None,
            help=(
                'specify an app_label or "ALL" to run for all app_labels in INSTALLED_APPS'),
        )

    def handle(self, *args, **options):
        app_label = options.get('app_label')
        if app_label == 'ALL':
            self.autodiscover()
        else:
            import_module(f'{app_label}.{self.module_name}')

    def autodiscover(self):
        """Autodiscovers rules in the "module_name".py file
        of any INSTALLED_APP.
        """
        sys.stdout.write(f' * checking for {self.module_name} ...\n')
        for app in django_apps.app_configs:
            try:
                mod = import_module(app)
                try:
                    import_module(f'{app}.{self.module_name}')
                except Exception as e:
                    if module_has_submodule(mod, self.module_name):
                        raise CommandError(e)
                else:
                    sys.stdout.write(
                        f'   - imported list data from \'{app}.{self.module_name}\'\n')
            except ImportError:
                pass
