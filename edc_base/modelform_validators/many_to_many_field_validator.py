from django.forms import ValidationError

from edc_constants.constants import NOT_APPLICABLE

from .base_form_validator import BaseFormValidator, NOT_APPLICABLE_ERROR, APPLICABLE_ERROR
from .base_form_validator import NOT_REQUIRED_ERROR, REQUIRED_ERROR, INVALID_ERROR


class ManyToManyFieldValidator(BaseFormValidator):

    def m2m_required_if(self, response=None, field=None, m2m_field=None, cleaned_data=None):
        """Raises an exception or returns False.

        m2m_field is required if field  == response
        """
        if (cleaned_data.get(field) == response
                and not cleaned_data.get(m2m_field)):
            message = {m2m_field: 'This field is required'}
            code = REQUIRED_ERROR
        elif (cleaned_data.get(field) == response
              and cleaned_data.get(m2m_field).count() == 0):
            message = {m2m_field: 'This field is required'}
            code = REQUIRED_ERROR
        elif (cleaned_data.get(field) != response
              and cleaned_data.get(m2m_field)
              and cleaned_data.get(m2m_field).count() != 0):
            message = {m2m_field: 'This field is not required'}
            code = NOT_REQUIRED_ERROR
        if message:
            self._errors.update(message)
            self._error_codes.append(code)
            raise ValidationError(message, code=code)
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
                    self._error_codes.append(INVALID_ERROR)
                    raise ValidationError(message, code=INVALID_ERROR)
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
                self._error_codes.append(REQUIRED_ERROR)
                raise ValidationError(message, code=REQUIRED_ERROR)
            elif not found and cleaned_data.get(field_other):
                message = {field_other: 'This field is not required.'}
                self._errors.update(message)
                self._error_codes.append(NOT_REQUIRED_ERROR)
                raise ValidationError(message, code=NOT_REQUIRED_ERROR)
        elif cleaned_data.get(field_other):
            message = {field_other: 'This field is not required.'}
            self._errors.update(message)
            self._error_codes.append(NOT_REQUIRED_ERROR)
            raise ValidationError(message, code=NOT_REQUIRED_ERROR)
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
                self._error_codes.append(APPLICABLE_ERROR)
                raise ValidationError(message, code=APPLICABLE_ERROR)
            elif not found and cleaned_data.get(field_other) != NOT_APPLICABLE:
                message = {field_other: 'This field is not applicable.'}
                self._errors.update(message)
                self._error_codes.append(NOT_APPLICABLE_ERROR)
                raise ValidationError(message, code=NOT_APPLICABLE_ERROR)
        elif cleaned_data.get(field_other) != NOT_APPLICABLE:
            message = {field_other: 'This field is not applicable.'}
            self._errors.update(message)
            self._error_codes.append(NOT_APPLICABLE_ERROR)
            raise ValidationError(message, code=NOT_APPLICABLE_ERROR)
        return False
