from django import forms
from edc_constants.constants import NOT_APPLICABLE


class Many2ManyModelValidationMixin:

    def m2m_required_if(self, response=None, field=None, m2m_field=None, cleaned_data=None):
        """Raises an exception or returns False.

        m2m_field is required if field  == response
        """
        if (cleaned_data.get(field) == response
                and not cleaned_data.get(m2m_field)):
            raise forms.ValidationError({
                m2m_field: 'This field is required'})
        elif (cleaned_data.get(field) == response
              and cleaned_data.get(m2m_field).count() == 0):
            raise forms.ValidationError({
                m2m_field: 'This field is required'})
        elif (cleaned_data.get(field) != response
              and cleaned_data.get(m2m_field)
              and cleaned_data.get(m2m_field).count() != 0):
            raise forms.ValidationError({
                m2m_field: 'This field is not required'})
        return False

    def m2m_single_selection_if(self, *single_selections, m2m_field=None, cleaned_data=None):
        """Raises an exception of returns False.

        if a selected response from m2m_field is in single_selections
        and there is more than one selected value, raises.
        """
        qs = cleaned_data.get(m2m_field)
        if qs and qs.count() > 1:
            selected = {obj.short_name: obj.name for obj in qs}
            for selection in single_selections:
                if selection in selected:
                    raise forms.ValidationError({
                        m2m_field:
                        'Invalid combination. \'{}\' may not be combined '
                        'with other selections'.format(
                            selected.get(selection))})
        return False

    def m2m_other_specify(self, *responses, m2m_field=None, field_other=None, cleaned_data=None):
        """Raises an exception or returns False.

        field_other is required if a selected response from m2m_field
        is in responses
        """
        qs = cleaned_data.get(m2m_field)
        found = False
        if qs and qs.count() > 0:
            selected = {obj.short_name: obj.name for obj in qs}
            for response in responses:
                if response in selected:
                    found = True
            if found and not cleaned_data.get(field_other):
                raise forms.ValidationError({
                    field_other:
                    'This field is required.'})
            elif not found and cleaned_data.get(field_other):
                raise forms.ValidationError({
                    field_other:
                    'This field is not required.'})
        elif cleaned_data.get(field_other):
            raise forms.ValidationError({
                field_other:
                'This field is not required.'})
        return False

    def m2m_other_specify_applicable(
            self, *responses, m2m_field=None, field_other=None, cleaned_data=None):
        """Raises an exception or returns False.

        field_other is applicable if a selected response from m2m_field
        is in responses
        """
        qs = cleaned_data.get(m2m_field)
        found = False
        if qs and qs.count() > 0:
            selected = {obj.short_name: obj.name for obj in qs}
            for response in responses:
                if response in selected:
                    found = True
            if found and cleaned_data.get(field_other) == NOT_APPLICABLE:
                raise forms.ValidationError({
                    field_other:
                    'This field is applicable.'})
            elif not found and cleaned_data.get(field_other) != NOT_APPLICABLE:
                raise forms.ValidationError({
                    field_other:
                    'This field is not applicable.'})
        elif cleaned_data.get(field_other) != NOT_APPLICABLE:
            raise forms.ValidationError({
                field_other:
                'This field is not applicable.'})
        return False
