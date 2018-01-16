from django.contrib.sites.managers import CurrentSiteManager as BaseCurrentSiteManager
from django.conf import settings


class CurrentSiteManager(BaseCurrentSiteManager):

    def get_queryset(self):
        if settings.SITE_ID == settings.REVIEWER_SITE_ID:
            queryset = super().get_queryset()
        else:
            return super().get_queryset().filter(
                **{self._get_field_name() + '__id': settings.SITE_ID})
        return queryset
