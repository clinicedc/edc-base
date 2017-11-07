from django.apps import apps as django_apps
from django.conf import settings
from django.views.generic.base import ContextMixin
from django_revision.views import RevisionMixin


class EdcBaseViewMixin(RevisionMixin, ContextMixin):
    """Mixes in common template variables for the footer, etc.
    """

    def get_context_data(self, **kwargs):
        app_config = django_apps.get_app_config('edc_base')
        edc_device_app_config = django_apps.get_app_config('edc_device')
        context = super().get_context_data(**kwargs)
        context.update({
            'DEBUG': settings.DEBUG,
            'copyright': app_config.copyright,
            'device_id': edc_device_app_config.device_id,
            'device_role': edc_device_app_config.device_role,
            'disclaimer': app_config.disclaimer,
            'institution': app_config.institution,
            'license': app_config.license,
            'project_name': app_config.project_name,
        })
        return context
