from django.apps import apps as django_apps
from django.conf import settings
from django_revision.views import RevisionMixin

from edc_base.exceptions import NavbarError


class EdcBaseViewMixin(RevisionMixin):
    """Mixes in common template variables for the navbar and footer, etc."""

    navbar_item_selected = None
    navbar_name = 'default'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.navbar = None
        self.navbars = django_apps.get_app_config('edc_base').navbars

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = self.get_edc_base_extra_context(context)
        context = self.get_navbar_context(context)
        context.update({
            'DEBUG': settings.DEBUG,
        })
        return context

    def get_navbar_context(self, context):
        self.navbar = self.navbars.get(self.navbar_name or 'default')
        if self.navbar_item_selected:
            if self.navbar_item_selected not in [navbar_item.name for navbar_item in self.navbar]:
                raise NavbarError(
                    'Navbar item does not exist. Got {}. Expected one of {}'.format(
                        self.navbar_item_selected, self.navbar))
        context.update({
            'navbar_item_selected': self.navbar_item_selected,
            'navbar': self.navbar,
            'navbar_name': self.navbar_name})
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
