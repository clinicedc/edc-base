from django import forms


class Many2ManyModelValidationMixin:

    def m2m_required_if(self, response=None, field=None, m2m_field=None):
        """Raises an exception or returns False.
        """
        cleaned_data = self.cleaned_data
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

    def m2m_single_selection_if(self, m2m_field=None, single_selections=None):
        cleaned_data = self.cleaned_data
        qs = cleaned_data.get(m2m_field)
        if qs and qs.count() > 1:
            selected = {obj.short_name: obj.name for obj in qs}
            print(selected)
            for selection in single_selections:
                if selection in selected:
                    print(selection)
                    raise forms.ValidationError({
                        m2m_field:
                        'Invalid combination. \'{}\' may not be combined '
                        'with other selections'.format(
                            selected.get(selection))})
        return False
