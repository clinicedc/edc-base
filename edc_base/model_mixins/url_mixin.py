from django.apps import apps as django_apps
from django.urls import reverse
from django.db import models


class UrlMixin(models.Model):

    def get_absolute_url(self):
        if self.id:
            absolute_url = reverse(self.admin_url_name, args=(str(self.id),))
        else:
            absolute_url = reverse(self.admin_url_name)
        return absolute_url

    @property
    def admin_url_name(self):
        """Returns the django admin add or change url name."""
        if self.id:
            admin_url_name = '{admin_site_name}:{app_label}_{object_name}_change'.format(
                admin_site_name=self.admin_site_name,
                app_label=self._meta.app_label,
                object_name=self._meta.object_name.lower()
            )
        else:
            admin_url_name = '{admin_site_name}:{app_label}_{object_name}_add'.format(
                admin_site_name=self.admin_site_name,
                app_label=self._meta.app_label,
                object_name=self._meta.object_name.lower())
        return admin_url_name

    @property
    def admin_site_name(self):
        try:
            # model specific
            admin_site_name = self.ADMIN_SITE_NAME
        except AttributeError:
            app_label = self._meta.app_label
            try:
                # app specific
                admin_site_name = django_apps.get_app_config(
                    app_label).admin_site_name
            except AttributeError:
                # default
                admin_site_name = 'admin'
        return admin_site_name

    class Meta:
        abstract = True
