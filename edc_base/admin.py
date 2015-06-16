from django.contrib import admin

from .modeladmin.admin import BaseModelAdmin

from .models import TestModel


class TestModelAdmin(BaseModelAdmin):
    readonly_fields = ('user_created', 'user_modified', 'created', 'modified', 'hostname_created', 'hostname_modified')
admin.site.register(TestModel, TestModelAdmin)
