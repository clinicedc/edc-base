from django import forms


class LogicCheck(object):
    """ Checks various conditions between field values and optional fields. """
    def __init__(self, model):

        self.model = model

    def test(self, cleaned_data, conditional_field, condition_value, optional_field,
             logic='required_if_value', required_optional_field_value=None):
        """Tests condition and raises a forms validation error on failure.

            Args:
                logic: label to indicate how to handle the field and values
                    * required_if_value (default): if conditional_field == condition_value ? required : not required
                    * not_required_if_value: if conditional_field == condition_value ? not required : required
                    * if_condition_then:
                    * if_condition_then_not:

        """
        conditional_field_value = cleaned_data.get(conditional_field, None)
        if isinstance(conditional_field_value, str):
            conditional_field_value = conditional_field_value.lower()

        if isinstance(condition_value, str):
            condition_value = condition_value.lower()

        optional_field_value = cleaned_data.get(optional_field, None)
        if isinstance(optional_field_value, str):
            optional_field_value = optional_field_value.lower()
        optional_field_verbose_name = None
        for field in self.model._meta.fields:
            if field.name == optional_field:
                optional_field_verbose_name = field.verbose_name
                break

        if logic == 'required_if_value':
            # default option
            # if conditional_field == condition_value ? required : not required
            if conditional_field_value:
                if conditional_field_value == condition_value and not optional_field_value:
                    raise forms.ValidationError(
                        'Please provide an answer for \'{}\'...'.format(optional_field_verbose_name,))
                if not conditional_field_value == condition_value and optional_field_value:
                    raise forms.ValidationError(
                        '{} is not required if {} is {}. Please correct'.format(
                            optional_field, conditional_field, condition_value,))

        if logic == 'not_required_if_value':
            # if conditional_field == condition_value ? not required : required
            if conditional_field_value:
                if conditional_field_value == condition_value and optional_field_value:
                    raise forms.ValidationError(
                        '{} is not required if {} is {}. Please correct'.format(
                            optional_field, conditional_field, condition_value,))
                if not conditional_field_value == condition_value and not optional_field_value:
                    raise forms.ValidationError(
                        'Please provide an answer for \'{}\'...'.format(optional_field_verbose_name,))

        if logic == 'if_condition_then':
            if conditional_field_value:
                if conditional_field_value == condition_value and not optional_field_value == required_optional_field_value:
                    raise forms.ValidationError(
                        '{} must be {} if {} is {}. Please correct'.format(
                            optional_field, required_optional_field_value, conditional_field, condition_value,))
                if not conditional_field_value == condition_value and optional_field_value == required_optional_field_value:
                    raise forms.ValidationError(
                        '{} cannot be {} if {} is not \'{}\'. Please correct'.format(
                            optional_field, optional_field_value, conditional_field, condition_value,))

        if logic == 'if_condition_then_not':
            if conditional_field_value:
                if conditional_field_value == condition_value and optional_field_value == required_optional_field_value:
                    raise forms.ValidationError(
                        '{} must not be {} if {} is {}. Please correct'.format(
                            optional_field, required_optional_field_value, conditional_field, condition_value,))
                if not conditional_field_value == condition_value and not optional_field_value == required_optional_field_value:
                    raise forms.ValidationError(
                        '{} must be {} if {} is {}. Please correct'.format(
                            optional_field, optional_field_value, conditional_field, condition_value,))
