from django.apps import apps as django_apps
from django.contrib import admin

from .fieldsets import Fieldsets


class FieldsetsModelAdminMixin(admin.ModelAdmin):

    # key: value where key is a viist_code. value is a fieldlist object
    conditional_fieldlists = {}
    # key: value where key is a visit code. value is a fieldsets object.
    conditional_fieldsets = {}

    def get_fieldsets(self, request, obj=None):
        """Returns fieldsets after making any modifications set in the
        "conditional" dictionaries."""
        fieldsets = super().get_fieldsets(request, obj=obj)
        fieldsets = Fieldsets(fieldsets=fieldsets)
        Appointment = django_apps.get_app_config('edc_appointment').model
        appointment = Appointment.objects.get(
            pk=request.GET.get('appointment'))
        fieldset = self.conditional_fieldsets.get(appointment.visit_code)
        if fieldset:
            fieldsets.add_fieldset(fieldset=fieldset())
        fieldlist = self.conditional_fieldlists.get(appointment.visit_code)
        if fieldlist:
            fieldsets.insert_fields(
                fieldlist.insert_fields,
                insert_after=fieldlist.insert_after,
                section=fieldlist.section)
            fieldsets.remove_fields(
                fieldlist.remove_fields,
                section=fieldlist.section)
        return fieldsets.fieldsets
