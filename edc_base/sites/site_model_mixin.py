from django.contrib.sites.managers import CurrentSiteManager
from django.contrib.sites.models import Site
from django.core.exceptions import ObjectDoesNotExist
from django.db import models


class SiteModelMixin(models.Model):

    site = models.ForeignKey(
        Site, on_delete=models.CASCADE, null=True, editable=False)

    on_site = CurrentSiteManager()

    def save(self, *args, **kwargs):
        try:
            if not self.site:
                self.site = Site.objects.get_current()
        except ObjectDoesNotExist:
            self.site = Site.objects.get_current()
        super().save(*args, **kwargs)

    class Meta:
        abstract = True
