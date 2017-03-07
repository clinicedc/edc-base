from django import forms

from edc_constants.constants import NOT_APPLICABLE


class ApplicableValidationMixin:

    def applicable_if(self, *responses, field=None, field_applicable=None):
        return self.applicable(
            *responses, field=field, field_applicable=field_applicable)

    def not_applicable_if(self, *responses, field=None, field_applicable=None):
        return self.not_applicable(
            *responses, field=field, field_applicable=field_applicable)

    def applicable(self, *responses, field=None, field_applicable=None):
        """Returns False or raises a validation error for field
        pattern where response to question 1 makes
        question 2 applicable.
        """
        cleaned_data = self.cleaned_data
        if field in cleaned_data and field_applicable in cleaned_data:
            if (cleaned_data.get(field) in responses
                    and cleaned_data.get(field_applicable) == NOT_APPLICABLE):
                raise forms.ValidationError({
                    field_applicable:
                    'This field is applicable'})
            elif (cleaned_data.get(field) not in responses
                    and cleaned_data.get(field_applicable) != NOT_APPLICABLE):
                raise forms.ValidationError({
                    field_applicable:
                    'This field is not applicable'})
        return False

    def not_applicable(self, *responses, field=None, field_applicable=None):
        """Returns False or raises a validation error for field
        pattern where response to question 1 makes
        question 2 NOT applicable.
        """
        cleaned_data = self.cleaned_data
        if field in cleaned_data and field_applicable in cleaned_data:
            if (cleaned_data.get(field) in responses
                    and cleaned_data.get(field_applicable) != NOT_APPLICABLE):
                raise forms.ValidationError({
                    field_applicable:
                    'This field is not applicable'})
            elif (cleaned_data.get(field) not in responses
                    and cleaned_data.get(field_applicable) == NOT_APPLICABLE):
                raise forms.ValidationError({
                    field_applicable:
                    'This field is applicable'})
        return False

    def applicable_if_true(self, condition, field_applicable=None,
                           applicable_msg=None, not_applicable_msg=None, **kwargs):
        cleaned_data = self.cleaned_data
        if field_applicable in cleaned_data:
            if (condition and self.cleaned_data.get(field_applicable) == NOT_APPLICABLE):
                raise forms.ValidationError({
                    field_applicable:
                    applicable_msg or 'This field is applicable.'})
            elif (not condition and self.cleaned_data.get(field_applicable) != NOT_APPLICABLE):
                raise forms.ValidationError({
                    field_applicable:
                    not_applicable_msg or 'This field is not applicable.'})
