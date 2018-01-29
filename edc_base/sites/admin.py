from django.conf import settings


class ReviewerSiteSaveError(Exception):
    pass


class ModelAdminSiteMixin:

    def save_model(self, request, obj, form, change):
        if 'django.contrib.sites' in settings.INSTALLED_APPS:
            if int(request.site.id) == int(settings.REVIEWER_SITE_ID):
                raise ReviewerSiteSaveError('Reviewers may not update data.')
        super().save_model(request, obj, form, change)
