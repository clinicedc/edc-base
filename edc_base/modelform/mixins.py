from django.db import models

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Field, Layout, ButtonHolder, Button

from django.contrib import admin
from django.utils import timezone


class AuditFieldsMixin:

    """Updates audit fields with username /datetime on create and modify."""
    def update_system_fields(self, request, instance, change):
        if not change:
            instance.user_created = request.user.username
            instance.created = timezone.now()
        instance.user_modified = request.user.username
        instance.date_modified = timezone.now()
        return instance

    def form_valid(self, form):
        form.instance = self.update_system_fields(self.request, form.instance, change=True)
        return super(AuditFieldsMixin, self).form_valid(form)


class CrispyFormMixin:

    """A mixin to setup a crispy form and configure using a modeladmin if specified.

    Does not inspect all of the modeladmin, just fields.

    If an FK is hidden using crispy_hidden_fields attr. The view will need to supply the value.

    Template should have the bootstrap datepicker plugin (Stefan Petre)

    {% block extra-css %}
        <link href="{% static "edc_base/datetimepicker/css/datetimepicker.css" %}" rel="stylesheet" type="text/css" >
    {% endblock extra-css %}

    {% block extra-scripts %}
        <script type="text/javascript" charset="utf8" src="{% static "edc_base/datetimepicker/js/bootstrap-datetimepicker.min.js" %}"></script>
    {% endblock extra-scripts %}
    """

    crispy_hidden_fields = None
    use_modeladmin = False
    admin_site = admin

    def __init__(self, *args, **kwargs):
        super(CrispyFormMixin, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-call-form'
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.helper.html5_required = True
        self.helper.layout = Layout(
            *self.get_crispy_fields(),
            ButtonHolder(
                Button('cancel-log-entry', 'Cancel'),
                Submit('submit-log-entry', 'Save', css_class="pull-right"),
            ))

    def get_crispy_fields(self):
        """Returns a list of field_names/classes for the helper.

        Field list is any of modeladmin.fields, form._meta.fields or model._meta.fields."""
        fields = self.get_modeladmin_fields() or self._meta.fields or [fld.name for fld in self._meta.model._meta.fields]
        fields = self.replace_hidden_fields(fields)
        fields = self.replace_date_fields(fields)
        return fields

    def get_modeladmin_fields(self):
        """Return a list of fields from the modeladmin."""
        fields = None
        if self.use_modeladmin:
            fields = self._meta.fields
            if self.admin_site.is_registered(self._meta.model):
                fields = list(self.admin_site._registry[self._meta.model].get_fields(None))
                self._meta.exclude = [fld.name for fld in self._meta.model._meta.fields if fld.name not in fields]
                self._meta.exclude = list(set(self._meta.exclude))
                self._meta.fields = None
        return fields

    def replace_hidden_fields(self, fields):
        """Return fields after replacing those in 'hidden_fields' with a hidden Field class."""
        fields = [field for field in fields if field not in self.hidden_fields]
        fields = ([Field(field, type='hidden') for field in (self.hidden_fields or [])] +
                  fields)
        return fields

    def replace_date_fields(self, fields):
        """Return fields after replacing DatetimeField or DateField with a datepicker Field class."""
        for fld in self._meta.model._meta.fields:
            try:
                pos = fields.index(fld.name)
                fields.pop(pos)
                if isinstance(fld, models.DateTimeField):
                    fields.insert(pos, self.as_datepicker(fld.name, use_time=True))
                elif isinstance(fld, models.DateField):
                    fields.insert(pos, self.as_datepicker(fld.name, use_time=False))
                else:
                    fields.insert(pos, fld.name)
            except ValueError:
                pass
        return fields

    def as_datepicker(self, field, use_time=None):
        """Return a datepicker Field class with or without time."""
        if use_time:
            data_date_format = 'yyyy-mm-dd hh:ii'
        else:
            data_date_format = 'yyyy-mm-dd'
        return Field(field, css_class='datetimepicker', data_date_format=data_date_format)
