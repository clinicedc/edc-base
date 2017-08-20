from django.views.generic.base import ContextMixin

from .navbar import Navbar


class NavbarViewMixin(ContextMixin):

    navbar_cls = Navbar
    navbar_item_selected = None
    navbar_name = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        navbar = self.navbar_cls(
            navbar_name=self.navbar_name,
            navbar_item_selected=self.navbar_item_selected)
        context.update(**navbar.context)
        return context
