from django import forms

from edc_constants.constants import NOT_APPLICABLE


class ApplicableValidationMixin:

    def applicable_if(self, response=None, field=None, field_applicable=None):
        return self.applicable(response, field, field_applicable)

    def not_applicable_if(self, response=None, field=None, field_applicable=None):
        return self.not_applicable(response, field, field_applicable)

    def applicable(self, response=None, field=None, field_applicable=None):
        """Returns False or raises a validation error for field
        pattern where response to question 1 makes
        question 2 applicable.
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

    def not_applicable(self, response=None, field=None, field_applicable=None):
        """Returns False or raises a validation error for field
        pattern where response to question 1 makes
        question 2 NOT applicable.
        """
        cleaned_data = self.cleaned_data
        if (cleaned_data.get(field) == response
                and cleaned_data.get(field_applicable) != NOT_APPLICABLE):
            raise forms.ValidationError({
                field_applicable:
                'This field is not applicable'})
        elif (cleaned_data.get(field) != response
                and cleaned_data.get(field_applicable) == NOT_APPLICABLE):
            raise forms.ValidationError({
                field_applicable:
                'This field is applicable'})
        return False
