from django.test import TestCase

from ..model.models import TestModel


class TestFields(TestCase):

    def test_uuid(self):
        new = TestModel()
        self.assertIsNone(new.id)
        new = TestModel.objects.create()
        self.assertIsNone(new.id)
