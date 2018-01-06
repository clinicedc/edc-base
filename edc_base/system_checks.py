import os

from django.core.checks import Warning
from django.conf import settings


def edc_base_check(app_configs, **kwargs):
    errors = []
    if not settings.DEBUG and settings.ETC_DIR and not settings.ETC_DIR.startswith('/etc'):
        errors.append(
            Warning(
                f'Insecure configuration. Use root level etc folder. '
                f'For example, \'/etc/{settings.APP_NAME}/\' '
                f'Got {settings.ETC_DIR}', id=f'settings.ETC_DIR'))
    if os.access(settings.ETC_DIR, os.W_OK):
        errors.append(
            Warning(
                f'Insecure configuration. Folder is writeable by this user. '
                f'Got {settings.ETC_DIR}', id=f'settings.ETC_DIR'))
    if os.access(settings.KEY_PATH, os.W_OK):
        errors.append(
            Warning(
                f'Insecure configuration. Folder is writeable by this user. '
                f'Got {settings.KEY_PATH}', id=f'settings.KEY_PATH'))
    if not os.path.exists(settings.STATIC_ROOT):
        errors.append(
            Warning(
                f'Folder does not exist. Got {settings.STATIC_ROOT}', id=f'settings.STATIC_ROOT'))
    return errors
