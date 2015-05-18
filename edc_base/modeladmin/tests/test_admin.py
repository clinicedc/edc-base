from django.contrib import admin
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.test import TestCase
from django.test.client import RequestFactory

from edc.base.modeladmin import NextUrlError
from edc.testing.models import TestModel

admin.autodiscover()


class TestAdmin(TestCase):

    urls = "urls"

    def setUp(self):
        self.factory = RequestFactory()
        self.user = self._create_superuser('django')
        # self.test_model = TestModelFactory()

    def _create_superuser(self, username):
        return User.objects.create(username=username, is_superuser=True)

    def _mocked_authenticated_request(self, url, user):
        request = self.factory.get(url)
        request.user = user
        return request

#     def _get_named_patterns(self):
#         "Returns list of (pattern-name, pattern) tuples"
#         from django.core import urlresolvers
#         resolver = urlresolvers.get_resolver(None)
#         patterns = sorted([
#             (key, value[0][0][0])
#             for key, value in resolver.reverse_dict.items()
#             if isinstance(key, basestring)
#         ])
#         return patterns

#     def _reverse_dashboard_url(self, url_name):
#         urls = []
#         self.test_model.pk, 'test_model'= dashboard_type, dashboard_id, dashboard_model, show
#         return urls
#
#     def test_dashboard_url(self):
#         print "specify next=add with missing GET parameters"
#         patterns = self._get_named_patterns()
#         longest = max([len(pair[0]) for pair in patterns])
#         for url_name, value in patterns:
#             if 'dashboard' in url_name:
#                 print '%s %s\n' % (url_name.ljust(longest + 1), value)
#                 urls = self._reverse_dashboard_url(url_name)
#
#         url = reverse('admin:testing_testmodel_add')
#         app_label, module_name = None, None
#         url = '{0}?next=add&app_label={1}&module_name={2}'.format(url, app_label or '', module_name or '')
#         print '  assert fails with url={0}'.format(url)
#         request = self._mocked_authenticated_request(url, self.user)
#         next_url_name = 'add'
#         self.assertRaises(NextUrlError, test_model_admin.response_add_redirect_on_next_url, next_url_name, request, test_model, None)

    def test_add_changlist_next_url_shortcuts(self):
        test_model = TestModel()
        test_model_admin = admin.site._registry.get(TestModel)

        print "specify next=add with missing GET parameters"
        url = reverse('admin:testing_testmodel_add')
        app_label, module_name = None, None
        url = '{0}?next=add&app_label={1}&module_name={2}'.format(url, app_label or '', module_name or '')
        print '  assert fails with url={0}'.format(url)
        request = self._mocked_authenticated_request(url, self.user)
        next_url_name = 'add'
        self.assertRaises(NextUrlError, test_model_admin.response_add_redirect_on_next_url, next_url_name, request, test_model, None)

        app_label, module_name = 'testing', None
        url = '{0}?next=add&app_label={1}&module_name={2}'.format(url, app_label or '', module_name or '')
        print '  assert fails with url={0}'.format(url)
        request = self._mocked_authenticated_request(url, self.user)
        self.assertRaises(NextUrlError, test_model_admin.response_add_redirect_on_next_url, next_url_name, request, test_model, None)

        app_label, module_name = 'testing', 'testmodel'
        url = '{0}?next=add&app_label={1}&module_name={2}'.format(url, app_label or '', module_name or '')
        print '  assert succeeds with url={0}'.format(url)
        request = self._mocked_authenticated_request(url, self.user)
        self.assertTrue(isinstance(test_model_admin.response_add_redirect_on_next_url(next_url_name, request, test_model, None), HttpResponseRedirect))

        print "specify next=changlist with missing GET parameters"
        next_url_name = 'changelist'
        url = reverse('admin:testing_testmodel_changelist')
        app_label, module_name = None, None
        url = '{0}?next=add&app_label={1}&module_name={2}'.format(url, app_label or '', module_name or '')
        print '  assert fails with url={0}'.format(url)
        request = self._mocked_authenticated_request(url, self.user)
        self.assertRaises(NextUrlError, test_model_admin.response_add_redirect_on_next_url, next_url_name, request, test_model, None)

        app_label, module_name = 'testing', None
        url = '{0}?next=add&app_label={1}&module_name={2}'.format(url, app_label or '', module_name or '')
        print '  assert fails with url={0}'.format(url)
        request = self._mocked_authenticated_request(url, self.user)
        self.assertRaises(NextUrlError, test_model_admin.response_add_redirect_on_next_url, next_url_name, request, test_model, None)

        app_label, module_name = 'testing', 'testmodel'
        url = '{0}?next=add&app_label={1}&module_name={2}'.format(url, app_label or '', module_name or '')
        print '  assert succeeds with url={0}'.format(url)
        request = self._mocked_authenticated_request(url, self.user)
        self.assertTrue(isinstance(test_model_admin.response_add_redirect_on_next_url(next_url_name, request, test_model, None), HttpResponseRedirect))
