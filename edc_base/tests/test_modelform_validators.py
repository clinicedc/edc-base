from django import forms
from django.test import TestCase, tag

from edc_constants.constants import YES, NO, DWTA, NOT_APPLICABLE

from ..modelform_validators import FormValidator, ValidationError
from ..modelform_validators import ModelFormFieldValidatorError, InvalidModelFormFieldValidator
from .models import TestModel
from pprint import pprint


class TestModelForm(forms.ModelForm):

    class Meta:
        model = TestModel
        fields = '__all__'


# class TestModelForms(TestCase):
#
#     def test_readonly_fields(self):
#         """Asserts required fields can be set to readonly not required
#         at the ModelForm level.
#         """
#
#         form = TestModelForm1(data={'f1': '1', 'f2': '2'})
#         self.assertFalse(form.is_valid())
#
#         class TestModelForm2(ReadonlyFieldsFormMixin, forms.ModelForm):
#
#             def get_readonly_fields(self):
#                 return ['f3', 'f4', 'f5']
#
#             class Meta:
#                 model = TestModel
#                 fields = '__all__'
#
#         form = TestModelForm2(data={'f1': '1', 'f2': '2'})
#         self.assertTrue(form.is_valid())


@tag('forms')
class TestFieldValidator(TestCase):

    def test_form_validator(self):
        """Asserts raises if cleaned data is None; that is, not
        provided.
        """
        try:
            FormValidator(cleaned_data={})
        except ModelFormFieldValidatorError as e:
            self.fail(f'ModelFormFieldValidatorError unexpectedly raised. Got {e}')

    def test_form_validator_cleaned_data_is_none(self):
        """Asserts raises if cleaned data is None; that is, not
        provided.
        """
        self.assertRaises(
            ModelFormFieldValidatorError, FormValidator, cleaned_data=None)

    def test_no_responses(self):
        """Asserts raises if no response provided.
        """
        form_validator = FormValidator(cleaned_data={})
        self.assertRaises(
            InvalidModelFormFieldValidator,
            form_validator.required_if)

    def test_no_field(self):
        """Asserts raises if no field provided.
        """
        form_validator = FormValidator(cleaned_data={})
        self.assertRaises(
            InvalidModelFormFieldValidator,
            form_validator.required_if, YES)

    def test_no_field_required(self):
        """Asserts raises if no field required provided.
        """
        form_validator = FormValidator(cleaned_data={})
        self.assertRaises(
            InvalidModelFormFieldValidator,
            form_validator.required_if, YES, field='field')


@tag('forms')
class TestRequiredFieldValidator1(TestCase):
    """Test required_if().
    """

    def test_ignored(self):
        form_validator = FormValidator(cleaned_data=dict(not_this_field=1))
        try:
            form_validator.required_if(
                YES, field='field_one', field_required='field_two')
        except (ModelFormFieldValidatorError, InvalidModelFormFieldValidator) as e:
            self.fail(f'Exception unexpectedly raised. Got {e}')

    def test_raises_for_missing_field_required_value(self):
        form_validator = FormValidator(cleaned_data=dict(field_one=YES))
        self.assertRaises(
            forms.ValidationError,
            form_validator.required_if,
            YES, field='field_one', field_required='field_two')

    def test_required_values_provided_ok(self):
        form_validator = FormValidator(
            cleaned_data=dict(field_one=YES, field_two='something'))
        try:
            form_validator.required_if(
                YES, field='field_one', field_required='field_two')
        except forms.ValidationError as e:
            self.fail(f'forms.ValidationError unexpectedly raised. Got {e}')

    def test_not_required_but_field_value_provided_raises(self):
        form_validator = FormValidator(
            cleaned_data=dict(field_one=NO, field_two='something'))
        self.assertRaises(
            forms.ValidationError,
            form_validator.required_if,
            YES, field='field_one', field_required='field_two')

    def test_required_field_value_not_applicable_ok(self):
        form_validator = FormValidator(
            cleaned_data=dict(field_one=NO, field_two=NOT_APPLICABLE))
        try:
            form_validator.required_if(
                YES, DWTA, field='field_one', field_required='field_two')
        except forms.ValidationError as e:
            self.fail(f'forms.ValidationError unexpectedly raised. Got {e}')

    def test_required_field_value_dwta_ok(self):
        form_validator = FormValidator(
            cleaned_data=dict(field_one=DWTA))
        try:
            form_validator.required_if(
                YES, DWTA, field='field_one', field_required='field_two',
                optional_if_dwta=True)
        except forms.ValidationError as e:
            self.fail(f'forms.ValidationError unexpectedly raised. Got {e}')


@tag('forms')
class TestRequiredFieldValidator2(TestCase):
    """Test not_required_if().
    """

    def test_ignored_blank1(self):
        """Asserts field_two not required if YES.
        """
        form_validator = FormValidator(cleaned_data=dict(field_one=YES))
        try:
            form_validator.not_required_if(
                YES, field='field_one', field_required='field_two')
        except (ModelFormFieldValidatorError, InvalidModelFormFieldValidator) as e:
            self.fail(f'Exception unexpectedly raised. Got {e}')

    def test_ignored_blank2(self):
        """Asserts field_two not required if YES so raises if field_two
        is specified.
        """
        form_validator = FormValidator(
            cleaned_data=dict(field_one=YES, field_two='blah'))
        self.assertRaises(
            forms.ValidationError,
            form_validator.not_required_if,
            YES, field='field_one', field_required='field_two')

    def test_ignored_not_applicable(self):
        """Asserts field_two not required if YES but NOT_APPLICABLE is
        same as not required.
        """
        form_validator = FormValidator(
            cleaned_data=dict(field_one=YES, field_two=NOT_APPLICABLE))
        try:
            form_validator.not_required_if(
                YES, field='field_one', field_required='field_two')
        except (ModelFormFieldValidatorError, InvalidModelFormFieldValidator) as e:
            self.fail(f'Exception unexpectedly raised. Got {e}')

    def test_required(self):
        """Asserts field_two required if not YES.
        """
        form_validator = FormValidator(cleaned_data=dict(field_one=NO))
        try:
            form_validator.not_required_if(
                YES, field='field_one', field_required='field_two')
        except (ModelFormFieldValidatorError, InvalidModelFormFieldValidator) as e:
            self.fail(f'Exception unexpectedly raised. Got {e}')


@tag('forms')
class TestFormValidatorInForm(TestCase):

    @tag('2')
    def test_form(self):

        class TestFormValidator(FormValidator):
            def clean(self):
                self.required_if(
                    YES,
                    field='f1',
                    field_required='f2')

        class TestModelForm(forms.ModelForm):

            def clean(self):
                cleaned_data = super().clean()
                form_validator = TestFormValidator(cleaned_data=cleaned_data)
                return form_validator.clean()

            class Meta:
                model = TestModel
                fields = '__all__'

        form = TestModelForm(data=dict(f1=NO, f2='blah'))
        self.assertFalse(form.is_valid())
        self.assertIn('f2', form._errors)
        form = TestModelForm(data=dict(f1=YES, f2='blah'))
        self.assertNotIn('f2', form._errors or {})
