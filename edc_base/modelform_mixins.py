from dateutil.relativedelta import relativedelta

from django import forms
from django.db import models
from django.contrib import admin

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Field, Layout, ButtonHolder, Button

from edc_constants.constants import YES, NO, UNKNOWN, OTHER, NOT_APPLICABLE

from .utils import get_utcnow


comparison_phrase = {
    'gt': 'must be greater than',
    'gte': 'must be greater than or equal to',
    'lt': 'must be less than',
    'lte': 'must be less than or equal to',
    'ne': 'may not equal', }


class CommonCleanModelFormMixin:

    def clean(self):
        """Raise exceptions raised by the common_clean method on the instance and re-raise
        as forms.ValidationErrors.

        Only exception classes listed in common_clean_exceptions are re-raised
        as forms.ValidationError.

        The exception instance, e, will use e.args[1] as the field name to
        place the form page error message on the field instead of at the top of the
        form page. """
        cleaned_data = super().clean()
        instance = self._meta.model(id=self.instance.id, **cleaned_data)
        try:
            instance.common_clean()
        except tuple(instance.common_clean_exceptions) as e:
            try:
                e = {e.args[1]: e.args[0]}
            except IndexError:
                pass
            raise forms.ValidationError(e)
        return cleaned_data


class AuditFieldsMixin:

    """Updates audit fields with username /datetime on create and modify."""
    def update_system_fields(self, request, instance, change):
        if not change:
            instance.user_created = request.user.username
            instance.created = get_utcnow()
        instance.user_modified = request.user.username
        instance.date_modified = get_utcnow()
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
        fields = (self.get_modeladmin_fields() or
                  self._meta.fields or
                  [fld.name for fld in self._meta.model._meta.fields if fld.editable])
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


class SimpleYesNoValidationMixin:

    def require_if_yes(self, yesno_field, required_field, required_msg=None, not_required_msg=None):
        if self.cleaned_data.get(yesno_field) in [NO, UNKNOWN] and self.cleaned_data.get(required_field):
            raise forms.ValidationError({
                required_field: [not_required_msg or 'This field is not required based on previous answer.']})
        elif self.cleaned_data.get(yesno_field) == YES and not self.cleaned_data.get(required_field):
            raise forms.ValidationError({
                required_field: [required_msg or 'This field is required based on previous answer.']})


class SimpleOtherSpecifyValidationMixin:

    def require_if_other(self, other_field, specify_field, required_msg=None, not_required_msg=None):
        if self.cleaned_data.get(other_field) != OTHER and self.cleaned_data.get(specify_field):
            raise forms.ValidationError({
                specify_field: [not_required_msg or 'This field is not required.']})
        elif self.cleaned_data.get(other_field) == OTHER and not self.cleaned_data.get(specify_field):
            raise forms.ValidationError({
                specify_field: [required_msg or 'Specify answer for OTHER.']})


class SimpleApplicableByAgeValidatorMixin:

    def validate_applicable_by_age(self, field, op, age, dob, previous_visit_date, subject_identifier, errmsg=None):
        age_delta = relativedelta(previous_visit_date, dob)
        applicable = True
        if self.cleaned_data.get(field):
            applicable = False
            if op == 'gt':
                if age_delta.years > age:
                    applicable = True
            elif op == 'gte':
                if age_delta.years >= age:
                    applicable = True
            elif op == 'lt':
                if age_delta.years < age:
                    applicable = True
            elif op == 'lte':
                if age_delta.years <= age:
                    applicable = True
            elif op == 'ne':
                if age_delta.years != age:
                    applicable = True
            elif op == 'eq':
                if age_delta.years == age:
                    applicable = True
        if not applicable and self.cleaned_data.get(field) != NOT_APPLICABLE:
                raise forms.ValidationError({
                    field: [errmsg or ('Not applicable. Age {phrase} {age}y at previous visit. '
                                       'Got {subject_age}y').format(
                        phrase=comparison_phrase.get(op),
                        age=age, subject_age=age_delta.years)]})
        if applicable and self.cleaned_data.get(field) == NOT_APPLICABLE:
                raise forms.ValidationError({
                    field: [errmsg or ('Applicable. Age {phrase} {age}y at previous visit to be "not applicable". '
                                       'Got {subject_age}y').format(
                        phrase=comparison_phrase.get(op),
                        age=age, subject_age=age_delta.years)]})


class SimpleDateFieldValidatorMixin:

    def validate_dates(self, field1=None, op=None, field2=None, errmsg=None,
                       verbose_name1=None, verbose_name2=None, value1=None, value2=None):
        """Validate that date1 is greater than date2."""
        date1 = self.cleaned_data.get(field1, value1)
        date2 = self.cleaned_data.get(field2, value2)
        if not self.compare_dates(date1, op, date2):
            raise forms.ValidationError({
                field1: [errmsg or '{field1} {phrase} {field2}.'.format(
                    field1=verbose_name1 or field1 or date1,
                    phrase=comparison_phrase.get(op),
                    field2=verbose_name2 or field2 or date2)]})

    def compare_dates(self, date1, op, date2):
        ret = True
        if date1 and date2:
            ret = False
            if op == 'gt':
                if date1 > date2:
                    ret = True
            elif op == 'gte':
                if date1 >= date2:
                    ret = True
            elif op == 'lt':
                if date1 < date2:
                    ret = True
            elif op == 'lte':
                if date1 <= date2:
                    ret = True
            elif op == 'ne':
                if date1 != date2:
                    ret = True
            elif op == 'eq':
                if date1 == date2:
                    ret = True
        return ret


class Many2ManyModelFormMixin:

    def validate_many_to_many_not_blank(self, field):
        """check if the many to many field is blank"""

        cleaned_data = self.cleaned_data

        if not cleaned_data.get(field):
            return True

    def validate_not_applicable_and_other_options(self, field):
        """check if not applicable has been selected along with other options"""

        cleaned_data = self.cleaned_data
        many2many_qs = cleaned_data.get(field).values_list('short_name', flat=True)
        many2many_list = list(many2many_qs.all())

        if NOT_APPLICABLE in many2many_list and len(many2many_list) > 1:
            return True

    def validate_not_applicable_not_there(self, field):
        """check if not applicable is not there when it is supposed to be"""

        cleaned_data = self.cleaned_data
        many2many_qs = cleaned_data.get(field).values_list('short_name', flat=True)
        many2many_list = list(many2many_qs.all())

        if NOT_APPLICABLE not in many2many_list:
            return True

    def validate_not_applicable_in_there(self, field):
        """check if not applicable is there"""

        cleaned_data = self.cleaned_data
        many2many_qs = cleaned_data.get(field).values_list('short_name', flat=True)
        many2many_list = list(many2many_qs.all())

        if NOT_APPLICABLE in many2many_list:
            return True
