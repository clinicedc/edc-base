from django.core.urlresolvers import reverse


class UrlMixin:

    ADMIN_SITE_NAME = 'admin'

    def get_absolute_url(self):
        if self.id:
            url = reverse('{admin_site}:{app_label}_{object_name}_change'.format(
                admin_site=self.ADMIN_SITE_NAME,
                app_label=self._meta.app_label,
                object_name=self._meta.object_name.lower()
            ), args=(str(self.id),))
        else:
            url = reverse('{admin_site}:{app_label}_{object_name}_add'.format(
                admin_site=self.ADMIN_SITE_NAME,
                app_label=self._meta.app_label,
                object_name=self._meta.object_name.lower())
            )
        return url
