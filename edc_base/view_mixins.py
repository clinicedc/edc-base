from django.apps import apps as django_apps
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage
from django_revision.views import RevisionMixin

from .utils import get_utcnow


class EdcBaseViewMixin(RevisionMixin):
    """Mixes in common template variables for the footer, etc."""

    def get_context_data(self, **kwargs):
        context = super(EdcBaseViewMixin, self).get_context_data(**kwargs)
        app_config = django_apps.get_app_config('edc_base')
        context.update({
            'project_name': app_config.project_name,
            'institution': app_config.institution,
            'year': get_utcnow().year,
            'DEBUG': settings.DEBUG,
        })
        return context

    def paginate(self, qs):
        paginator = Paginator(qs, self.paginate_by)
        try:
            page = paginator.page(self.kwargs.get('page', 1))
        except EmptyPage:
            page = paginator.page(paginator.num_pages)
        return page
