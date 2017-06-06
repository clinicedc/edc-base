from django import forms
from django.test import TestCase, tag

from ..modelform_mixins import ReadonlyFieldsFormMixin, RequiredFieldValidationMixin
from .models import TestModel
from edc_constants.constants import YES


class TestModelForm1(forms.ModelForm):

    class Meta:
        model = TestModel
        fields = '__all__'


class TestModelForms(TestCase):

    def test_readonly_fields(self):
        """Asserts required fields can be set to readonly not required
        at the ModelForm level."""

        form = TestModelForm1(data={'f1': '1', 'f2': '2'})
        self.assertFalse(form.is_valid())

        class TestModelForm2(ReadonlyFieldsFormMixin, forms.ModelForm):

            def get_readonly_fields(self):
                return ['f3', 'f4', 'f5']

            class Meta:
                model = TestModel
                fields = '__all__'

        form = TestModelForm2(data={'f1': '1', 'f2': '2'})
        self.assertTrue(form.is_valid())

    def test_required_if(self):
        mixin = RequiredFieldValidationMixin()
        mixin.cleaned_data = {}
        self.assertFalse(mixin.required_if(
            YES, field='blah', field_required='more_blah'))
        mixin.cleaned_data = {'blah': YES}
        self.assertRaises(
            forms.ValidationError,
            mixin.required_if,
            YES, field='blah', field_required='more_blah')
