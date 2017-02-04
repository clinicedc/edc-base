from django import forms

from edc_constants.constants import NOT_APPLICABLE


class ApplicableValidationMixin:

    def applicable_if(self, response=None, field=None, field_applicable=None):
        return self.applicable(response, field, field_applicable)

    def applicable(self, response=None, field=None, field_applicable=None):
        """Returns False or raises a validation error for field
        pattern where response to question 1 determines if
        question 2 is applicable or not.
        """
        cleaned_data = self.cleaned_data
        if (cleaned_data.get(field) == response
                and cleaned_data.get(field_applicable) == NOT_APPLICABLE):
            raise forms.ValidationError({
                field_applicable:
                'This field is applicable'})
        elif (cleaned_data.get(field) != response
                and cleaned_data.get(field_applicable) != NOT_APPLICABLE):
            raise forms.ValidationError({
                field_applicable:
                'This field is not applicable'})
        return False
