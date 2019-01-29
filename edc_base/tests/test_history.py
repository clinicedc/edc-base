import re

from django.core import serializers
from django.test import TestCase, tag  # noqa
from edc_constants.constants import UUID_PATTERN

from .models import TestModelWithHistory


class TestHistory(TestCase):

    databases = '__all__'

    def test_history_creates(self):
        obj = TestModelWithHistory.objects.create()
        self.assertEqual(obj.history.all().count(), 1)

    def test_history_id_is_uuid(self):
        obj = TestModelWithHistory.objects.create()
        pattern = re.compile(UUID_PATTERN)
        self.assertTrue(
            pattern.match(str(obj.history.all()[0].id)))
        self.assertTrue(
            pattern.match(str(obj.history.all()[0].history_id)))

    def test_history_has_natural_key_method(self):
        obj = TestModelWithHistory.objects.create()
        pattern = re.compile(UUID_PATTERN)
        self.assertTrue(
            pattern.match(str(obj.history.all()[0].natural_key()[0])))

    def test_history_has_custom_get_by_natural_key(self):
        obj = TestModelWithHistory.objects.create()
        try:
            obj.history.all()[0].__class__.objects.get_by_natural_key(
                obj.history.all()[0].history_id)
        except AttributeError:
            self.fail('\'get_by_natural_key\' unexpectedly does not exist')

    def test_history_is_serializable_deserializable(self):

        model_obj = TestModelWithHistory.objects.create()

        json_text = serializers.serialize(
            'json', model_obj.history.all(),
            ensure_ascii=True,
            use_natural_foreign_keys=True,
            use_natural_primary_keys=False)

        model_obj.history.all().delete()
        model_obj.refresh_from_db()
        self.assertEqual(model_obj.history.all().count(), 0)

        gen = serializers.deserialize(
            "json", json_text,
            ensure_ascii=True,
            use_natural_foreign_keys=True,
            use_natural_primary_keys=True)

        for obj in gen:
            obj.object.save()

        model_obj.refresh_from_db()
        self.assertEqual(model_obj.history.all().count(), 1)

    def test_history_is_serializable_deserializable_using(self):

        model_obj = TestModelWithHistory.objects.using('client').create()

        json_text = serializers.serialize(
            'json', model_obj.history.using('client').all(),
            ensure_ascii=True,
            use_natural_foreign_keys=True,
            use_natural_primary_keys=False)

        model_obj.history.using('client').all().delete()
        model_obj.refresh_from_db()
        self.assertEqual(model_obj.history.using('client').all().count(), 0)

        gen = serializers.deserialize(
            "json", json_text,
            ensure_ascii=True,
            use_natural_foreign_keys=True,
            use_natural_primary_keys=True)

        for obj in gen:
            obj.object.save(using='client')

        model_obj.refresh_from_db()
        self.assertEqual(model_obj.history.using('client').all().count(), 1)
