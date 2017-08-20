from django.apps import apps as django_apps

from .navbar_item import NavbarError


class Navbar:

    def __init__(self, navbar_item_selected=None, navbar_name=None):
        self.navbar = None
        self.navbar_item_selected = navbar_item_selected
        self.navbar_name = navbar_name or 'default'

    @property
    def context(self):
        navbars = django_apps.get_app_config('edc_base').navbars
        self.navbar = navbars.get(self.navbar_name)
        if self.navbar_item_selected:
            if self.navbar_item_selected not in [navbar_item.name for navbar_item in self.navbar]:
                navbar_item_names = [item.name for item in self.navbar]
                raise NavbarError(
                    f'Navbar item does not exist. Got \'{self.navbar_item_selected}\'. '
                    f'Expected one of {navbar_item_names}. See navbar \'{self.navbar_name}\'.')
        return dict(
            navbar_item_selected=self.navbar_item_selected,
            navbar=self.navbar,
            navbar_name=self.navbar_name)
