from django.conf import settings
from django.contrib.sites.models import Site


class ReviewerSiteSaveError(Exception):
    pass


class ModelAdminSitesMixin:

    def save_model(self, request, obj, form, change):

        if 'django.contrib.sites' in settings.INSTALLED_APPS:

            if Site.objects.get_current() == settings.REVIEWER_SITE_ID:
                raise ReviewerSiteSaveError('Reviewers may not update data.')
        super().save_model(request, obj, form, change)
