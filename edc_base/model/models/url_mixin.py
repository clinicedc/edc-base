from django.core.urlresolvers import reverse
from django.db import models


class UrlMixin(models.Model):

    ADMIN_SITE_NAME = None

    def get_absolute_url(self):
        if self.id:
            url = reverse(self.admin_url_name, args=(str(self.id),))
        else:
            url = reverse(self.admin_url_name)
        return url

    @property
    def admin_url_name(self):
        """Returns the django admin add or change url name."""
        if self.id:
            admin_url_name = '{admin_site}:{app_label}_{object_name}_change'.format(
                admin_site=self.ADMIN_SITE_NAME or 'admin',
                app_label=self._meta.app_label,
                object_name=self._meta.object_name.lower()
            )
        else:
            admin_url_name = '{admin_site}:{app_label}_{object_name}_add'.format(
                admin_site=self.ADMIN_SITE_NAME or 'admin',
                app_label=self._meta.app_label,
                object_name=self._meta.object_name.lower())
        return admin_url_name

    class Meta:
        abstract = True
