from django import forms


class RequiredFieldValidationMixin:

    def required_if(self, *responses, field=None, field_required=None,
                    required_msg=None, not_required_msg=None, **kwargs):
        """Raises an exception or returns False.

        if field in responses then field_required is required.
        """
        cleaned_data = self.cleaned_data
        if field in cleaned_data and field_required in cleaned_data:
            if (self.cleaned_data.get(field) in responses
                    and not self.cleaned_data.get(field_required)):
                raise forms.ValidationError({
                    field_required:
                    required_msg or 'This field is required.'})
            elif (self.cleaned_data.get(field) not in responses
                    and self.cleaned_data.get(field_required)):
                raise forms.ValidationError({
                    field_required:
                    not_required_msg or 'This field is not required.'})
        return False

    def required_if_true(self, condition, field_required=None,
                         required_msg=None, not_required_msg=None, **kwargs):
        cleaned_data = self.cleaned_data
        if field_required in cleaned_data:
            if (condition and not self.cleaned_data.get(field_required)):
                raise forms.ValidationError({
                    field_required:
                    required_msg or 'This field is required.'})
            elif (not condition and self.cleaned_data.get(field_required)):
                raise forms.ValidationError({
                    field_required:
                    not_required_msg or 'This field is not required.'})

    def not_required_if(self, *responses, field=None, field_required=None,
                        required_msg=None, not_required_msg=None,
                        inverse=None, **kwargs):
        """Raises an exception or returns False.

        if field NOT in responses then field_required is required.
        """
        cleaned_data = self.cleaned_data
        inverse = True if inverse is None else inverse
        if field in cleaned_data and field_required in cleaned_data:
            if (self.cleaned_data.get(field) in responses
                    and self.cleaned_data.get(field_required)):
                raise forms.ValidationError({
                    field_required:
                    not_required_msg or 'This field is not required.'})
            elif inverse and (self.cleaned_data.get(field) not in responses
                              and not self.cleaned_data.get(field_required)):
                raise forms.ValidationError({
                    field_required:
                    required_msg or 'This field is required.'})
        return False
