from django.contrib.sites.models import Site
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.conf import settings


class SiteModelMixin(models.Model):

    site = models.ForeignKey(
        Site, on_delete=models.PROTECT, null=True, editable=False)

    def save(self, *args, **kwargs):
        current = Site.objects.get_current()
        if current != settings.REVIEWER_SITE_ID:
            try:
                if not self.site:
                    self.site = Site.objects.get_current()
            except ObjectDoesNotExist:
                self.site = Site.objects.get_current()
        super().save(*args, **kwargs)

    class Meta:
        abstract = True
