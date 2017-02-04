from copy import copy
from inspect import ismethod

from django import forms
from django.db.models import ManyToManyField

from edc_base.exceptions import CommonCleanError


class CommonCleanException:

    def __init__(self, e):
        self.exception = e
        self.msg = e.args[0]
        if self.field:
            self.msg = {self.field: self.msg}

    @property
    def field(self):
        try:
            return self.exception.args[1]
        except IndexError:
            return None


class CommonCleanModelFormMixin:

    def clean(self):
        """Raise exceptions raised by the common_clean method on the
        instance and re-raise as forms.ValidationErrors.

        M2M fields are automatically excluded.

        Only exception classes listed in common_clean_exceptions are
        re-raised as forms.ValidationError.

        The exception instance, e, will use e.args[1] as the field name
        to place the form page error message on the field instead of at
        the top of the form page.
        """
        cleaned_data = super().clean()
        instance = copy(self.instance)
        m2ms = [field.name for field in self._meta.model._meta.get_fields()
                if isinstance(field, ManyToManyField)]
        for key, value in cleaned_data.items():
            if key not in m2ms:
                setattr(instance, key, value)
        if instance.common_clean_exceptions:
            # common mistake, i guess
            if ismethod(instance.common_clean_exceptions):
                raise CommonCleanError(
                    'Expected \'common_clean_exceptions\' to be a '
                    'property not method. Got {}'.format(
                        instance.__class__, instance.common_clean_exceptions()))
            try:
                instance.common_clean()
            except tuple(instance.common_clean_exceptions) as e:
                self.common_clean_raise_exception(e)
        return cleaned_data

    def common_clean_raise_exception(self, e):
        exception = CommonCleanException(e)
        raise forms.ValidationError(exception.msg)
