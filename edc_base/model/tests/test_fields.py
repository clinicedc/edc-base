from git import Repo, GitCmdObjectDB

from django.conf import settings
from django.test import TestCase

from edc.testing.models import TestModel


class TestFields(TestCase):

    def test_revision_field2(self):
        """can create a new model instance and revision is not none."""
        test_model = TestModel()
        test_model.save()
        self.assertIsNotNone(test_model.revision)

    def test_revision_field3(self):
        """can create a new model instance using objects.create() and revision is not none."""
        test_model = TestModel.objects.create()
        self.assertIsNotNone(test_model.revision)

    def test_revision_field4(self):
        """new model instance has the current revision set."""
        repo = Repo(settings.PROJECT_ROOT, odbt=GitCmdObjectDB)
        test_model = TestModel.objects.create()
        self.assertEqual(
            test_model.revision,
            '{0}:{1}'.format(str(repo.active_branch), str(repo.active_branch.commit)))

    def test_revision_field5(self):
        """create new model instance, try to set revision to an arbitrary value."""
        repo = Repo(settings.PROJECT_ROOT, odbt=GitCmdObjectDB)
        test_model = TestModel.objects.create()
        test_model.revision = 'erik'
        test_model.save()
        self.assertEqual(test_model.revision, '{0}:{1}'.format(
            str(repo.active_branch), str(repo.active_branch.commit)))
