from datetime import date

from django.apps import apps as django_apps
from django_revision.views import RevisionMixin
# from django.utils.decorators import method_decorator
# from django.contrib.auth.decorators import login_required


class EdcBaseViewMixin(RevisionMixin):
    """Mixes in common template variables for the footer, etc."""

#     @method_decorator(login_required)
#     def dispatch(self, *args, **kwargs):
#         return super(EdcBaseViewMixin, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        app_config = django_apps.get_app_config('edc_base')
        context.update({
            'project_name': app_config.verbose_name,
            'institution': app_config.institution,
            'year': date.today().year,
        })
        return context
