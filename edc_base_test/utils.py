import arrow

from django.apps import apps as django_apps


def get_utcnow():
    """Returns a datetime that is the earliest date of consent allowed for the consent model."""

    edc_protocol_app_config = django_apps.get_app_config('edc_protocol')
    study_open_datetime = edc_protocol_app_config.study_open_datetime
    return arrow.Arrow.fromdatetime(study_open_datetime, tzinfo=study_open_datetime.tzinfo).to('utc').datetime
