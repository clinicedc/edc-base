from django.core.exceptions import ObjectDoesNotExist


def add_or_update_django_sites(apps, edc_sites=None, edc_fqdn=None):
    Site = apps.get_model('sites', 'Site')
    Site.objects.get(name='example.com').delete()
    for site_id, site_name in edc_sites:
        try:
            site_obj = Site.objects.get(pk=site_id)
        except ObjectDoesNotExist:
            Site.objects.create(
                pk=site_id,
                name=site_name,
                domain=f'{site_name}.{edc_fqdn}')
        else:
            site_obj.name = site_name
            site_obj.domain = f'{site_name}.{edc_fqdn}'
            site_obj.save
