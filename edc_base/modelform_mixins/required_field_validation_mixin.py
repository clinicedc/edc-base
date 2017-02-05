from django import forms


class RequiredFieldValidationMixin:

    def required_if(self, *responses, field=None, field_required=None,
                    required_msg=None, not_required_msg=None, **kwargs):
        """Riases an exception or returns False.

        if field in responses then field_required is required.
        """
        if (self.cleaned_data.get(field) in responses
                and not self.cleaned_data.get(field_required)):
            raise forms.ValidationError({
                field_required:
                not_required_msg or 'This field is required.'})
        elif (self.cleaned_data.get(field) not in responses
                and self.cleaned_data.get(field_required)):
            raise forms.ValidationError({
                field_required:
                not_required_msg or 'This field is not required.'})
        return False

    def required_if_true(self, condition, field_required=None,
                         required_msg=None, not_required_msg=None, **kwargs):
        if (condition and not self.cleaned_data.get(field_required)):
            raise forms.ValidationError({
                field_required:
                not_required_msg or 'This field is required.'})
        elif (not condition and self.cleaned_data.get(field_required)):
            raise forms.ValidationError({
                field_required:
                not_required_msg or 'This field is not required.'})
