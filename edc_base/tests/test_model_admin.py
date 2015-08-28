import os
import pwd
import uuid
import socket

from django.contrib import admin
from django.contrib.auth.models import User
from django.db import models
from django.test import TransactionTestCase
from edc_base.model.models.base_model import BaseModel
from edc_base.modeladmin.admin.base_model_admin import BaseModelAdmin
from django.test.client import RequestFactory
from django.core.urlresolvers import reverse


class MyTestModel(BaseModel):

    field1 = models.CharField(
        max_length=10,
        null=True
    )

    class Meta:
        app_label = 'edc_base'


class MyTestModelAdmin(BaseModelAdmin):
    pass
admin.site.register(MyTestModel, MyTestModelAdmin)


class TestModelAdmin(TransactionTestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='erikvw', email='1@1.com', password='password')

    def test_modified(self):
        obj = MyTestModel.objects.create()
        obj.save()
        obj = MyTestModel.objects.get(pk=obj.pk)
        self.assertIsNotNone(obj.modified)
        modified = obj.modified
        obj.save()
        self.assertNotEqual(obj.modified, modified)

    def test_modified_admin(self):
        obj = MyTestModel.objects.create()
        modified = obj.modified
        request = self.factory.get(reverse('admin:index'))
        request.user = self.user
        my_model_admin = admin.site._registry[MyTestModel]
        my_model_admin.save_model(request, obj, None, True)
        obj = MyTestModel.objects.get(pk=obj.pk)
        self.assertNotEqual(obj.modified, modified)

    def test_user_admin(self):
        """Asserts admin save_model updates created and modified username."""
        obj = MyTestModel.objects.create()
        self.assertFalse(obj.user_created)
        self.assertFalse(obj.user_modified)
        request = self.factory.get(reverse('admin:index'))
        request.user = self.user
        my_model_admin = admin.site._registry[MyTestModel]
        my_model_admin.save_model(request, obj, None, True)
        obj = MyTestModel.objects.get(pk=obj.pk)
        self.assertEqual(obj.user_created, self.user.username)
        self.assertEqual(obj.user_modified, self.user.username)
        next_user = User.objects.create_user(
            username='erikvw2', email='1@2.com', password='password')
        request.user = next_user
        my_model_admin.save_model(request, obj, None, True)
        obj = MyTestModel.objects.get(pk=obj.pk)
        self.assertEqual(obj.user_created, self.user.username)
        self.assertEqual(obj.user_modified, next_user.username)
