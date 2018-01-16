from django.contrib.sites.managers import CurrentSiteManager as BaseCurrentSiteManager
from django.conf import settings


class CurrentSiteManager(BaseCurrentSiteManager):

    def get_queryset(self):
        site_id = settings.SITE_ID
        if site_id == '0':
            queryset = super().get_queryset()
        else:
            return super().get_queryset().filter(
                **{self._get_field_name() + '__id': settings.SITE_ID})
        return queryset
