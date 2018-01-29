from django.db import models
from django.contrib.sites.managers import CurrentSiteManager as BaseCurrentSiteManager
from django.conf import settings


class CurrentSiteManager(BaseCurrentSiteManager):

    def get_queryset(self):
        if int(settings.SITE_ID) == int(settings.REVIEWER_SITE_ID):
            queryset = models.Manager.get_queryset(self)
        else:
            return super().get_queryset().filter(
                **{self._get_field_name() + '__id': settings.SITE_ID})
        return queryset
