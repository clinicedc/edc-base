from django.test import TestCase, tag

from ..modeladmin_mixins import ModelAdminNextUrlRedirectMixin
from edc_base.tests.models import TestModel
from django.test.client import RequestFactory
from edc_base.modeladmin_mixins.model_admin_next_url_redirect_mixin import ModelAdminNextUrlRedirectError


class TestModelAdmin(TestCase):

    def setUp(self):
        self.factory = RequestFactory()

    def test_next_url(self):
        obj = TestModel()
        request = self.factory.get(
            '/?next=my_url_name,arg1,arg2&agr1=value1&arg2=value2&arg3=value3&arg4=value4')
        mixin = ModelAdminNextUrlRedirectMixin()
        self.assertRaises(
            ModelAdminNextUrlRedirectError,
            mixin.redirect_url, request, obj)

    def test_next_url1(self):
        obj = TestModel()
        request = self.factory.get(
            '/?next=my_url_name,arg1,arg2&arg1=value1&arg2=value2&arg3=value3&arg4=value4')
        mixin = ModelAdminNextUrlRedirectMixin()
        try:
            mixin.redirect_url(request, obj)
        except ModelAdminNextUrlRedirectError as e:
            self.assertIn('my_url_name', str(e))

    def test_next_url4(self):
        obj = TestModel()
        request = self.factory.get(
            '/?next=my_url_name,arg1,arg2&arg1=value1&arg2=value2&arg3=value3&arg4=value4')
        mixin = ModelAdminNextUrlRedirectMixin()
        try:
            mixin.redirect_url(request, obj)
        except ModelAdminNextUrlRedirectError as e:
            self.assertIn("{'arg1': 'value1', 'arg2': 'value2'}", str(e))