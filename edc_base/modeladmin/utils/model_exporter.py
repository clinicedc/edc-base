import os
from django.contrib import admin
from django.conf import settings
from django.contrib.auth.models import User
from edc.subject.visit_schedule.models import VisitDefinition


class ModelExporter(object):

    def __init__(self, *args, **kwargs):
        self.response = None
        self._client = None
        self._visit_definition = None
        try:
            self.admin_user = User.objects.create(username='django', password='cc3721b')
            self.admin_user.set_password('1234')
            self.admin_user.is_staff = True
            self.admin_user.is_active = True
            self.admin_user.is_superuser = True
            self.admin_user.save()
        except:
            pass

    def export(self, request, code):
        """ """
        self.set_visit_definition(code)
        path = settings.MEDIA_ROOT
        request.method = "GET"
        for entry in self.get_visit_definition().entry_set.all().order_by('entry_order'):
            model_class = entry.content_type_map.model_class()
            model_admin = admin.site._registry.get(model_class)
            t = model_admin.add_view(request)
            if not t.status_code == 200:
                raise TypeError('failed for model {0}. Got status_code {1}'.format(model_class, t.status_code))
            content = t.render()
            fn = '{0}.html'.format(model_class._meta.object_name.lower())
            path = os.path.join(settings.MEDIA_ROOT, fn)
            fo = open(path, 'w')
            fo.write(content.rendered_content.replace('/static', '{0}'.format(settings.STATIC_ROOT)).replace('/admin/jsi18n/', '{0}/admin/jsi18n/'.format(settings.STATIC_ROOT)))
            fo.close()

    def set_visit_definition(self, code):
        self._visit_definition = VisitDefinition.objects.get(code=code)

    def get_visit_definition(self):
        if not self._visit_definition:
            self.set_visit_definition()
        return self._visit_definition
