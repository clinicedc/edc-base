from django.apps import apps as django_apps
from django.conf import settings
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.views.generic.base import ContextMixin
from django_revision.views import RevisionMixin


class EdcBaseViewMixin(RevisionMixin, ContextMixin):
    """Mixes in common template variables for the footer, etc.
    """

    def get_context_data(self, **kwargs):

        self.request.session.set_test_cookie()
        if not self.request.session.test_cookie_worked():
            messages.add_message(
                self.request, messages.ERROR, 'Please enable cookies.')
        self.request.session.delete_test_cookie()
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
            'site': get_current_site(self.request),
        })
        if settings.DEBUG:
            messages.add_message(
                self.request, messages.ERROR,
                ('This EDC is running in DEBUG-mode. Use for testing only. '
                 'Do not use this system for production data collection!'))
        return context
