from django.apps import apps as django_apps
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django_revision.views import RevisionMixin


class EdcBaseViewMixin(RevisionMixin):
    """Mixes in common template variables for the footer, etc."""

    base_html = 'edc_base/base.html'

    def get_context_data(self, **kwargs):
        context = super(EdcBaseViewMixin, self).get_context_data(**kwargs)
        context = self.get_edc_base_extra_context(context)
        context.update({
            'DEBUG': settings.DEBUG,
            'base_html': self.base_html,
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
