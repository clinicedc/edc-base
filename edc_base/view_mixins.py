from django.apps import apps as django_apps
from django.conf import settings
from django_revision.views import RevisionMixin

from .navbar import NavbarViewMixin


class EdcBaseViewMixin(NavbarViewMixin, RevisionMixin):
    """Mixes in common template variables for the navbar and footer, etc.
    """

    def get_context_data(self, **kwargs):
        edc_device_app_config = django_apps.get_app_config('edc_device')
        context = super().get_context_data(**kwargs)
        context = self.get_edc_base_extra_context(context)
        context.update({
            'DEBUG': settings.DEBUG,
            'device_id': edc_device_app_config.device_id,
            'device_role': edc_device_app_config.device_role,
        })
        return context

    def get_edc_base_extra_context(self, extra_context):
        app_config = django_apps.get_app_config('edc_base')
        extra_context.update({
            'project_name': app_config.project_name,
            'institution': app_config.institution,
            'copyright': app_config.copyright,
            'license': app_config.license,
            'disclaimer': app_config.disclaimer})
        return extra_context
