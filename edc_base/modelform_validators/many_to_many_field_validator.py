from django.forms import ValidationError

from edc_constants.constants import NOT_APPLICABLE

from .base_form_validator import BaseFormValidator


class ManyToManyFieldValidator(BaseFormValidator):

    def m2m_required_if(self, response=None, field=None, m2m_field=None, cleaned_data=None):
        """Raises an exception or returns False.

        m2m_field is required if field  == response
        """
        message = None
        if (cleaned_data.get(field) == response
                and not cleaned_data.get(m2m_field)):
            message = {m2m_field: 'This field is required'}
        elif (cleaned_data.get(field) == response
              and cleaned_data.get(m2m_field).count() == 0):
            message = {m2m_field: 'This field is required'}
        elif (cleaned_data.get(field) != response
              and cleaned_data.get(m2m_field)
              and cleaned_data.get(m2m_field).count() != 0):
            message = {m2m_field: 'This field is not required'}
        if message:
            self._errors.update(message)
            raise ValidationError(message)
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
                    message = {
                        m2m_field:
                        f'Invalid combination. \'{selected.get(selection)}\' may not be combined '
                        f'with other selections'}
                    self._errors.update(message)
                    raise ValidationError(message)
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
                message = {field_other: 'This field is required.'}
                self._errors.update(message)
                raise ValidationError(message)
            elif not found and cleaned_data.get(field_other):
                message = {field_other: 'This field is not required.'}
                self._errors.update(message)
                raise ValidationError(message)
        elif cleaned_data.get(field_other):
            message = {field_other: 'This field is not required.'}
            self._errors.update(message)
            raise ValidationError(message)
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
                message = {field_other: 'This field is applicable.'}
                self._errors.update(message)
                raise ValidationError(message)
            elif not found and cleaned_data.get(field_other) != NOT_APPLICABLE:
                message = {field_other: 'This field is not applicable.'}
                self._errors.update(message)
                raise ValidationError(message)
        elif cleaned_data.get(field_other) != NOT_APPLICABLE:
            message = {field_other: 'This field is not applicable.'}
            self._errors.update(message)
            raise ValidationError(message)
        return False
