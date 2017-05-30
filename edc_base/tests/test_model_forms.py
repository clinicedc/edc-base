from django import forms
from django.test import TestCase, tag

from ..modelform_mixins import ReadonlyFieldsFormMixin
from .models import TestModel


@tag('me')
class TestModelForms(TestCase):

    def test_readonly_fields(self):
        """Asserts required fields can be set to readonly not required
        at the ModelForm level."""
        class TestModelForm1(forms.ModelForm):

            class Meta:
                model = TestModel
                fields = '__all__'

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
