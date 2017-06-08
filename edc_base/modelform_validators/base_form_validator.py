
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

    def __init__(self, cleaned_data=None):
        self._errors = {}
        self.cleaned_data = cleaned_data
        if cleaned_data is None:
            raise ModelFormFieldValidatorError(
                f'{repr(self)}. Expected a cleaned_data dictionary. Got None.')

    def __repr__(self):
        return f'{self.__class__.__name__}(cleaned_data={self.cleaned_data})'

    def __str__(self):
        return self.cleaned_data
