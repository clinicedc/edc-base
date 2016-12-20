from django.apps import apps as django_apps
from edc_base.test_mixins.exceptions import TestMixinError


class ReferenceDateMixin:
    """Sets the reference date to the earliest consent date based on the consent model.

    Note that edc_consent and edc_protocol during tests will set the open and close date
    range to be in the past. See edc_consent.apps.AppConfig, edc_protocol.apps.AppConfig"""

    consent_model = None

    def get_utcnow(self):
        """Returns a datetime that is the earliest date of consent allowed for the consent model.

        Note: this date is defined in edc_consent.apps ConsentConfig."""
        app_config = django_apps.get_app_config('edc_consent')
        test_mixin_reference_datetime = {}
        for consent_config in app_config.consent_configs:
            test_mixin_reference_datetime.update({consent_config.label_lower: consent_config.start})
        if not test_mixin_reference_datetime:
            raise TestMixinError('Cannot determine a reference date from get_utcnow')
        if self.consent_model not in test_mixin_reference_datetime:
            raise TestMixinError(
                'Cannot determine a reference date from get_utcnow. No config for \'{}\'. '
                'Expected one of {}.See AppConfig and your TestMixin class'.format(
                    self.consent_model, [c.label_lower for c in app_config.consent_configs]))
        utcnow = test_mixin_reference_datetime.get(self.consent_model)
        if not utcnow:
            raise TestMixinError('Cannot determine a reference date from get_utcnow. Got {}.'.format(utcnow))
        return utcnow
