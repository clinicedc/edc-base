from django import forms
from edc_constants.constants import DWTA, NOT_APPLICABLE


class RequiredFieldValidationMixin:

    def required_if(self, *responses, field=None, field_required=None,
                    required_msg=None, not_required_msg=None,
                    optional_if_dwta=None, cleaned_data=None, **kwargs):
        """Raises an exception or returns False.

        if field in responses then field_required is required.
        """
        if field in cleaned_data and field_required in cleaned_data:
            if (DWTA in responses and optional_if_dwta
                    and cleaned_data.get(field) == DWTA):
                pass
            elif (cleaned_data.get(field) in responses
                    and (not cleaned_data.get(field_required)
                         or cleaned_data.get(field_required) == NOT_APPLICABLE)):
                raise forms.ValidationError({
                    field_required:
                    required_msg or 'This field is required.'})
            elif (cleaned_data.get(field) not in responses
                    and (cleaned_data.get(field_required)
                         and cleaned_data.get(field_required) != NOT_APPLICABLE)):
                raise forms.ValidationError({
                    field_required:
                    not_required_msg or 'This field is not required.'})
        return False

    def required_if_true(self, cleaned_data, condition, field_required=None,
                         required_msg=None, not_required_msg=None, **kwargs):
        if field_required in cleaned_data:
            if (condition and (not cleaned_data.get(field_required)
                               or cleaned_data.get(field_required) == NOT_APPLICABLE)):
                raise forms.ValidationError({
                    field_required:
                    required_msg or 'This field is required.'})
            elif (not condition and cleaned_data.get(field_required)
                    and cleaned_data.get(field_required) != NOT_APPLICABLE):
                raise forms.ValidationError({
                    field_required:
                    not_required_msg or 'This field is not required.'})

    def not_required_if(self, cleaned_data, *responses, field=None, field_required=None,
                        required_msg=None, not_required_msg=None,
                        optional_if_dwta=None, inverse=None, **kwargs):
        """Raises an exception or returns False.

        if field NOT in responses then field_required is required.
        """
        inverse = True if inverse is None else inverse
        if field in cleaned_data and field_required in cleaned_data:
            if (DWTA in responses and optional_if_dwta
                    and cleaned_data.get(field) == DWTA):
                pass
            elif (cleaned_data.get(field) in responses
                    and (cleaned_data.get(field_required)
                         and cleaned_data.get(field_required) != NOT_APPLICABLE)):
                raise forms.ValidationError({
                    field_required:
                    not_required_msg or 'This field is not required.'})
            elif inverse and (cleaned_data.get(field) not in responses
                              and (not cleaned_data.get(field_required)
                                   or cleaned_data.get(field_required) == NOT_APPLICABLE)):
                raise forms.ValidationError({
                    field_required:
                    required_msg or 'This field is required.'})
        return False
