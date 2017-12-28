from django.contrib.sites.models import Site
from django.db import models
from django.core.exceptions import ObjectDoesNotExist


class SiteModelMixin(models.Model):

    site = models.ForeignKey(Site, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        try:
            self.site
        except ObjectDoesNotExist:
            self.site = Site.objects.get_current()
        super().save(*args, **kwargs)

    class Meta:
        abstract = True
