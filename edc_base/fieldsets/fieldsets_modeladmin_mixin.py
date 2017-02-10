from django.apps import apps as django_apps
from django.contrib import admin

from .fieldsets import Fieldsets


class FieldsetsModelAdminMixin(admin.ModelAdmin):

    """A class that helps modify fieldsets for subject models

    * Model is expected to have a relation to have subject_visit__appointment.
    * Expects appointment to be in GET"""

    # key: value where key is a visit_code. value is a fieldlist object
    conditional_fieldlists = {}
    # key: value where key is a visit code. value is a fieldsets object.
    conditional_fieldsets = {}

    custom_form_labels = {}

    def update_form_labels(self, request, form):
        """Returns a form instance after modifying form labels
        referred to in custom_form_labels."""
        for field, options in self.custom_form_labels.items():
            if field in form.base_fields:
                obj = self.get_previous_instance(request)
                if obj:
                    if options.get('callback')(obj):
                        form.base_fields[field].label = options.get('label').format(
                            previous=obj.report_datetime.strftime('%B %Y'))
        return form

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj=obj, **kwargs)
        return self.update_form_labels(request, form)

    def get_previous_instance(self, request, instance=None, **kwargs):
        """Returns a model instance that is the previous relative to
        this object's subject_visit.

        Override this method if not a subject model"""
        obj = None
        appointment = instance or self.get_instance(request)
        if appointment:
            # FIXME: dont hardcode subject_visit as attr name to the
            # visit model.
            obj = self.model.objects.filter(
                subject_visit__appointment__subject_identifier=appointment.subject_identifier).order_by(
                    'report_datetime').last()
        return obj

    def get_appointment(self, request):
        """Returns the appointment instance for this request or None.
        """
        Appointment = django_apps.get_app_config('edc_appointment').model
        try:
            return Appointment.objects.get(
                pk=request.GET.get('appointment'))
        except Appointment.DoesNotExist:
            return None

    def get_instance(self, request):
        """Returns the instance that provides the key
        for the "conditional" dictionaries.

        For example: appointment.
        """
        return self.get_appointment(request)

    def get_key(self, request, obj=None):
        """Returns a string that is the key to `get` the
        value in the "conditional" dictionaries.

        For example:
            appointment.visit_code == '1000' will be used
            to look into:
                conditional_fieldsets = {
                    '1000': ...}
        """
        try:
            return self.get_instance(request).visit_code
        except AttributeError:
            return None

    def get_fieldsets(self, request, obj=None):
        """Returns fieldsets after modifications declared in
        "conditional" dictionaries.
        """
        fieldsets = super().get_fieldsets(request, obj=obj)
        fieldsets = Fieldsets(fieldsets=fieldsets)
        key = self.get_key(request, obj)
        fieldset = self.conditional_fieldsets.get(key)
        if fieldset:
            fieldsets.add_fieldset(fieldset=fieldset)
        fieldlist = self.conditional_fieldlists.get(key)
        if fieldlist:
            try:
                fieldsets.insert_fields(
                    fieldlist.insert_fields,
                    insert_after=fieldlist.insert_after,
                    section=fieldlist.section)
            except AttributeError:
                pass
            try:
                fieldsets.remove_fields(
                    fieldlist.remove_fields,
                    section=fieldlist.section)
            except AttributeError:
                pass
        fieldsets = self.update_fieldset_for_form(
            fieldsets, request)
        return fieldsets.fieldsets

    def update_fieldset_for_form(self, fieldsets, request, **kwargs):
        """Not ready"""
        if self.custom_form_labels:
            instance = self.get_instance(request)
            if instance:
                obj = self.get_previous_instance(request, instance=instance)
                if obj:
                    pass  # do something
            else:
                pass  # possibly remove field"
#                 fieldsets.remove_fields(
#                     'last_seen_circumcised')
        return fieldsets
