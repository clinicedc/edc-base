from django.forms import ValidationError

from edc_constants.constants import OTHER

from .base_form_validator import BaseFormValidator


class OtherSpecifyFieldValidator(BaseFormValidator):
    """A modelform mixin that handles 'OTHER/Other specify'
    field pattern.
    """

    def validate_other_specify(self, field, other_specify_field=None,
                               required_msg=None, not_required_msg=None,
                               other_stored_value=None,
                               ref=None, **kwargs):
        """Returns False or raises a ValidationError.
        """
        cleaned_data = self.cleaned_data
        other = other_stored_value or OTHER

        # assume field naming convention
        if not other_specify_field:
            other_specify_field = f'{field}_other'

        if (cleaned_data.get(field)
                and cleaned_data.get(field) == other
                and not cleaned_data.get(other_specify_field)):
            ref = '' if not ref else f' ref: {ref}'
            message = {
                other_specify_field:
                required_msg or f'This field is required.{ref}'}
            self._errors.update(message)
            raise ValidationError(message)
        elif (cleaned_data.get(field)
                and cleaned_data.get(field) != other
                and cleaned_data.get(other_specify_field)):
            ref = '' if not ref else f' ref: {ref}'
            message = {
                other_specify_field:
                not_required_msg or f'This field is not required.{ref}'}
            self._errors.update(message)
            raise ValidationError(message)
        return False
