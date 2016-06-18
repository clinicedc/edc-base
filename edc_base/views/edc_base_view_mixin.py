from datetime import date

from django.apps import apps as django_apps
from django.conf import settings
from django_revision.revision import Revision


class EdcBaseViewMixin:
    """Mixes in common template variables for the footer, etc."""

    app_label = None  # this is the main app (e.g. where settings resides)

    @property
    def app(self):
        try:
            app_label = settings.APP_LABEL
        except AttributeError:
            app_label = self.app_label
        return django_apps.get_app_config(app_label)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'project_name': self.app.verbose_name,
            'institution': self.app.institution,
            'year': date.today().year,
            'revision': Revision().tag,
        })
        return context
