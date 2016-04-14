from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

try:
    from simple_history.models import HistoricalRecords as AuditTrail
    if 'simple_history' not in settings.INSTALLED_APPS:
        raise ImproperlyConfigured(
            'Why is the package \'django_simple_history\' installed? '
            'If you mean to use it, add it to INSTALLED_APPS, otherwise uninstall it '
            'with \'pip uninstall django-simple-history\'.')
except ImportError:
    from edc_audit.audit_trail import AuditTrail
