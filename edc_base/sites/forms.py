from django import forms
from django.conf import settings


class SiteModelFormMixin:

    def clean(self):
        from django.contrib.sites.models import Site
        site = Site.objects.get_current()
        if int(site.id) == int(settings.REVIEWER_SITE_ID):
            raise forms.ValidationError(
                'Adding or changing data has been disabled. '
                f'See Site configuration. Got \'{site.name.title()}\'.')
        return super().clean()
