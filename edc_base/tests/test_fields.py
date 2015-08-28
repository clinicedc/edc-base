import os
import pwd
import uuid
import socket

from django.test import TestCase

from django.db import models

from edc_base.model.models import BaseUuidModel, HistoricalRecords


class TestModel(BaseUuidModel):

    f1 = models.CharField(max_length=10)
    f2 = models.CharField(max_length=10)
    f3 = models.CharField(max_length=10, null=True, blank=False)
    f4 = models.CharField(max_length=10, null=True, blank=False)
    f5 = models.CharField(max_length=10)

    history = HistoricalRecords()

    class Meta:
        app_label = 'edc_base'


class TestFields(TestCase):

    def test_uuid_none_on_instance(self):
        test_model = TestModel()
        self.assertIsNone(test_model.id)

    def test_uuid_set_on_create(self):
        test_model = TestModel.objects.create()
        self.assertIsNotNone(test_model.id)
        self.assertIsInstance(test_model.id, uuid.UUID)

    def test_uuid_set_on_save(self):
        test_model = TestModel()
        self.assertIsNone(test_model.id)
        test_model.save()
        self.assertIsInstance(test_model.id, uuid.UUID)

    def test_uuid_unique(self):
        test_model1 = TestModel.objects.create()
        self.assertIsNotNone(test_model1.id)
        self.assertIsInstance(test_model1.id, uuid.UUID)
        test_model2 = TestModel.objects.create()
        self.assertIsNotNone(test_model2.id)
        self.assertIsInstance(test_model2.id, uuid.UUID)
        test_model3 = TestModel()
        self.assertIsNone(test_model3.id)
        test_model3.save()
        self.assertIsInstance(test_model3.id, uuid.UUID)
        self.assertFalse(test_model1 == test_model2)
        self.assertFalse(test_model2 == test_model3)

    def test_hostname_modification(self):
        hostname = socket.gethostname()
        test_model = TestModel()
        self.assertFalse(test_model.hostname_modified)
        test_model = TestModel.objects.create()
        self.assertIsInstance(test_model.hostname_modified, str)
        self.assertEquals(hostname, test_model.hostname_modified)
        test_model.save()
        self.assertEquals(hostname, test_model.hostname_modified)

    def test_hostname_created(self):
        hostname = socket.gethostname()
        test_model = TestModel()
        self.assertIsInstance(test_model.hostname_created, str)
        self.assertEquals(hostname, test_model.hostname_created)
        test_model = TestModel.objects.create()
        self.assertEquals(hostname, test_model.hostname_created)
        test_model.save()
        self.assertEquals(hostname, test_model.hostname_created)

    def test_user_created(self):
        """Assert user is set on created ONLY unless explicitly set."""
        user = pwd.getpwuid(os.getuid()).pw_name
        test_model = TestModel.objects.create()
        self.assertEquals('', test_model.user_created)
        test_model.user_created = ''
        test_model.save()
        test_model = TestModel(user_created='jason')
        test_model.save()
        self.assertEquals('jason', test_model.user_created)
        test_model.save()
        self.assertEquals('jason', test_model.user_created)

    def test_user_modified(self):
        """Assert user is always updated."""
        user = pwd.getpwuid(os.getuid()).pw_name
        test_model = TestModel()
        test_model.save()
        self.assertEquals('', test_model.user_modified)
        test_model = TestModel.objects.create()
        self.assertEquals('', test_model.user_modified)
        test_model.user_modified = ''
        test_model.save()
        self.assertEquals(user, test_model.user_modified)
