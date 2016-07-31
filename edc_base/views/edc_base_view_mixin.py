from datetime import date

from django.apps import apps as django_apps
from django.conf import settings
from django_revision.views import RevisionMixin
from django.core.exceptions import ImproperlyConfigured
# from django.utils.decorators import method_decorator
# from django.contrib.auth.decorators import login_required


class EdcBaseViewMixin(RevisionMixin):
    """Mixes in common template variables for the footer, etc."""

    app_config_name = None  # this is the main app that defines institution, etc

    @property
    def main_app_config(self):
        try:
            name = settings.APP_CONFIG_NAME
        except AttributeError:
            name = self.app_config_name
        if not name:
            raise ImproperlyConfigured(
                'Main AppConfig "name" is needed for AppConfig attributes \'verbose_name\', \'institution\', etc. '
                'Add to settings APP_CONFIG_NAME = your_app_name.')
        return django_apps.get_app_config(name)

#     @method_decorator(login_required)
#     def dispatch(self, *args, **kwargs):
#         return super(EdcBaseViewMixin, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'project_name': self.main_app_config.verbose_name,
            'institution': self.main_app_config.institution,
            'year': date.today().year,
        })
        return context
