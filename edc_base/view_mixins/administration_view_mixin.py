from django.apps import apps as django_apps
from django.contrib.auth.decorators import login_required
from django.urls.base import reverse
from django.urls.exceptions import NoReverseMatch
from django.utils.decorators import method_decorator
from django.views.generic.base import ContextMixin


class AdministrationViewMixin(ContextMixin):

    template_name = 'edc_base/administration.html'
    base_template_name = 'edc_base/base.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(base_template_name=self.base_template_name)
        context.update(sections=self.sections)
        return context

    def get_section(self, app_config=None):
        """Returns a dictionary for a single section.

        Format is {verbose_name: url_name}
        """
        section = {}
        try:
            url_namespace = app_config.url_namespace
        except AttributeError:
            url_namespace = app_config.name
        try:
            url = app_config.home_url_name
        except AttributeError:
            url = f'{url_namespace}:home_url'
        try:
            reverse(url)
        except NoReverseMatch:
            pass
        else:
            section = {app_config.verbose_name: url}
        return section

    @property
    def sections(self):
        """Returns a dictionary (sorted) of the administration sections
        to show on the Administration page.
        """
        sections = {}
        for app_config in django_apps.get_app_configs():
            try:
                include = app_config.include_in_administration_section
            except AttributeError:
                include = True
            if include:
                sections.update(**self.get_section(app_config))
        keys = list(sections.keys())
        keys.sort()
        return {key: sections.get(key) for key in keys}
