import os

from django.conf import settings
from string import Template

ID = 0
NAME = 1

filename_template = '$site_name.$app_name.clinicedc.org.py'

template = """# $site_name.$app_name gunicorn.conf
import os

from pathlib import Path

SOURCE_ROOT = str(Path(os.path.dirname(os.path.abspath(__file__))).parent)

errorlog = os.path.join(SOURCE_ROOT, 'log/$app_name-gunicorn-error.log')
accesslog = os.path.join(SOURCE_ROOT, 'log/$app_name-gunicorn-access.log')
loglevel = 'debug'
pidfile = os.path.join(SOURCE_ROOT, 'run/$app_name-$site_name.pid')

workers = 2  # the number of recommended workers is '2 * number of CPUs + 1'

raw_env = [f'DJANGO_SETTINGS_MODULE=$app_name.settings.production.$site_name']

bind = "127.0.0.1:90$site_id"
"""


def create_gunicorn_conf_files(path=None, sites=None):
    """Generates gunicorn conf files for each site.

    "sites" is a tuple of ((site_id, site_name), ...)

    for example:
        $ python manage.py shell
        >>> import os
        >>> from edc_base.config import create_gunicorn_conf_files
        >>> from ambition.sites import ambition_sites
        >>> path = os.path.expanduser('~/source/ambition/gunicorn')
        >>> create_gunicorn_conf_files(path=path, sites=ambition_sites)
    """
    app_name = settings.APP_NAME
    for site in sites:
        site_id = str(site[ID]).zfill(2)
        s = Template(template).safe_substitute(
            site_id=site_id, site_name=site[NAME], app_name=app_name)
        filename = Template(filename_template).safe_substitute(
            site_name=site[NAME], app_name=app_name)
        with open(os.path.join(path, filename), 'w+') as f:
            f.write(s)
