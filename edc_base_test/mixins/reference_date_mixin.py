from edc_base_test.utils import get_utcnow


class ReferenceDateMixin:
    """Sets the reference date to the earliest consent date based on the consent model.

    Note that edc_consent and edc_protocol during tests will set the open and close date
    range to be in the past. See edc_consent.apps.AppConfig, edc_protocol.apps.AppConfig"""

    def get_utcnow(self):
        return get_utcnow()
