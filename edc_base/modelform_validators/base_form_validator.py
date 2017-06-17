from django.forms import forms


APPLICABLE_ERROR = 'applicable'
INVALID_ERROR = 'invalid'
NOT_APPLICABLE_ERROR = 'not_applicable'
NOT_REQUIRED_ERROR = 'not_required'
REQUIRED_ERROR = 'required'


class InvalidModelFormFieldValidator(Exception):

    def __init__(self, message, code=None):
        message = f'Invalid field validator. Got \'{message}\''
        super().__init__(message)
        self.code = code


class ModelFormFieldValidatorError(Exception):

    def __init__(self, message, code=None):
        super().__init__(message)
        self.code = code


class BaseFormValidator:

    def __init__(self, cleaned_data=None, instance=None):
        self._errors = {}
        self._error_codes = []
        self.cleaned_data = cleaned_data
        self.instance = instance
        if cleaned_data is None:
            raise ModelFormFieldValidatorError(
                f'{repr(self)}. Expected a cleaned_data dictionary. Got None.')

    def __repr__(self):
        return f'{self.__class__.__name__}(cleaned_data={self.cleaned_data})'

    def __str__(self):
        return self.cleaned_data

    def clean(self):
        pass

    def validate(self):
        try:
            self.clean()
        except forms.ValidationError as e:
            self.capture_error_message(e)
            self.capture_error_code(e)
            raise forms.ValidationError(e)
        return self.cleaned_data

    def capture_error_message(self, e):
        try:
            self._errors.update(**e.error_dict)
        except AttributeError:
            try:
                self._errors.update(__all__=e.error_list)
            except AttributeError:
                self._errors.update(__all__=str(e))

    def capture_error_code(self, e):
        try:
            self._error_codes.append(e.code)
        except AttributeError:
            pass
