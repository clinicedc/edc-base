from django.contrib.sites.models import Site


class SiteTestCaseMixin:

    default_sites = [
        (10, 'mochudi', 'mochudi'),
        (20, 'molepolole', 'molepolole'),
        (30, 'lobatse', 'lobatse'),
        (40, 'gaborone', 'gaborone'),
        (50, 'karakobis', 'karakobis')]

    @property
    def site_names(self):
        return [s[1] for s in self.default_sites]

    def setUp(self):
        super().setUp()
        Site.objects.all().delete()
        for site_id, site_name, _ in self.default_sites:
            Site.objects.create(
                pk=site_id, name=site_name, domain=f'{site_name}.edc.bhp.org.bw')
