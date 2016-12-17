from django.apps import apps as django_apps


class ReferenceDateMixin:
    """Sets the reference date to the earliest consent date based on the consent model.

    Note that edc_consent and edc_protocol during tests will set the open and close date
    range to be in the past. See edc_consent.apps.AppConfig, edc_protocol.apps.AppConfig"""

    consent_model = None

    @property
    def test_mixin_reference_datetime(self):
        app_config = django_apps.get_app_config('edc_consent')
        test_mixin_reference_datetime = {}
        for consent_config in app_config.consent_configs:
            test_mixin_reference_datetime.update({consent_config.label_lower: consent_config.start})
        return test_mixin_reference_datetime

    def get_utcnow(self):
        """Returns a datetime that is the earliest date of consent allowed for the consent model.

        Note: this date is defined in edc_consent.apps ConsentConfig."""
        return self.test_mixin_reference_datetime.get(self.consent_model)
