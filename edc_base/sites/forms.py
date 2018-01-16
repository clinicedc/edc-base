from django import forms
from django.conf import settings


class SiteModelFormMixin:

    def clean(self):
        from django.contrib.sites.models import Site
        if Site.objects.get_current() == int(settings.REVIEWER_SITE_ID):
            raise forms.ValidationError(
                'Reviewers may not add or update CRF data. '
                'You are logged into the "Reviewer\'s system. '
                'Try logging into one of the site specific systems.')
        return super().clean()
