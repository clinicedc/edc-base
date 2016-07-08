from datetime import date

from django.apps import apps as django_apps
from django.conf import settings
from django_revision.views import RevisionMixin
from django.core.exceptions import ImproperlyConfigured
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required


class EdcBaseViewMixin(RevisionMixin):
    """Mixes in common template variables for the footer, etc."""

    app_label = None  # this is the main app (e.g. where settings resides)

    @property
    def app(self):
        try:
            app_label = settings.APP_LABEL
        except AttributeError:
            app_label = self.app_label
        if not app_label:
            raise ImproperlyConfigured('Main APP_LABEL not set. Either set on view or in settings.APP_LABEL.')
        return django_apps.get_app_config(app_label)

#     @method_decorator(login_required)
#     def dispatch(self, *args, **kwargs):
#         return super(EdcBaseViewMixin, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'project_name': self.app.verbose_name,
            'institution': self.app.institution,
            'year': date.today().year,
        })
        return context
