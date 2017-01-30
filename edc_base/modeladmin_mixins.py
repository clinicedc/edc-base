import re

from django.apps import apps as django_apps
from django.core.urlresolvers import reverse
from django.http.response import HttpResponseRedirect
from django.utils.html import format_html
from django.contrib.admin.widgets import AdminDateWidget
from django.forms.widgets import DateInput

from .utils import get_utcnow
from django.utils.safestring import mark_safe


audit_fields = ('user_created', 'user_modified',
                'created', 'modified', 'hostname_created', 'hostname_modified')

audit_fieldset_tuple = (
    'Audit', {
        'classes': ('collapse',),
        'fields': audit_fields})


class ModelAdminBasicMixin:

    """Merge ModelAdmin attributes with the concrete class attributes
    fields, radio_fields, list_display, list_filter and search_fields.

    `mixin_exclude_fields` is a list of fields included in the mixin
    but not wanted on the concrete.

    Use for a ModelAdmin mixin prepared for an abstract models,
    e.g. edc_consent.models.BaseConsent.
    """

    mixin_fields = []

    mixin_radio_fields = {}

    mixin_list_display = []
    list_display_pos = []

    mixin_list_filter = []
    list_filter_pos = []

    mixin_search_fields = []

    mixin_exclude_fields = []

    def reorder(self, original_list):
        """Return an ordered list after inserting list items from the
        original that were passed tuples of (index, item).
        """
        new_list = []
        items_with_pos = []
        for index, item in enumerate(original_list):
            try:
                _, _ = item
                items_with_pos.append(item)
            except (ValueError, TypeError):
                new_list.append(item)
        for index, item in items_with_pos:
            try:
                new_list.pop(new_list.index(item))
            except ValueError:
                pass
            new_list.insert(index, item)
        return new_list

    def get_list_display(self, request):
        self.list_display = list(
            super(ModelAdminBasicMixin, self).get_list_display(request) or [])
        self.list_display = self.reorder(
            list(self.list_display) + list(self.list_display_pos or []))
        self.list_display = self.extend_from(
            self.list_display, self.mixin_list_display or [])
        self.list_display = self.remove_from(self.list_display)
        return tuple(self.list_display)

    def get_list_filter(self, request):
        self.list_filter = list(
            super(ModelAdminBasicMixin, self).get_list_filter(request) or [])
        self.list_filter = self.reorder(
            list(self.list_filter) + list(self.list_filter_pos or []))
        self.list_filter = self.update_from_mixin(
            self.list_filter, self.mixin_list_filter or [])
        return tuple(self.list_filter)

    def get_search_fields(self, request):
        self.search_fields = list(
            super(ModelAdminBasicMixin, self).get_search_fields(request) or [])
        self.search_fields = self.update_from_mixin(
            self.search_fields, self.mixin_search_fields or [])
        return tuple(self.search_fields)

    def get_fields(self, request, obj=None):
        self.radio_fields = self.get_radio_fields(request, obj)
        if self.mixin_fields:
            self.fields = self.update_from_mixin(
                self.fields, self.mixin_fields or [])
            return self.fields
        elif self.fields:
            return self.fields
        form = self.get_form(request, obj, fields=None)
        return list(form.base_fields) + list(self.get_readonly_fields(request, obj))

    def update_from_mixin(self, field_list, mixin_field_list):
        field_list = self.extend_from(field_list or [], mixin_field_list or [])
        field_list = self.remove_from(field_list or [])
        return tuple(field_list)

    def extend_from(self, field_list, mixin_field_list):
        return (list(field_list)
                + list([fld for fld in mixin_field_list if fld not in field_list]))

    def remove_from(self, field_list):
        field_list = list(field_list)
        for field in self.mixin_exclude_fields:
            try:
                field_list.remove(field)
            except ValueError:
                pass
        return tuple(field_list)

    def get_radio_fields(self, request, obj=None):
        self.radio_fields.update(self.mixin_radio_fields)
        for key in self.mixin_exclude_fields:
            try:
                del self.mixin_radio_fields[key]
            except KeyError:
                pass
        return self.radio_fields


class ModelAdminInstitutionMixin:

    """Adds instituion attrs to the ModelAdmin context.
    """

    def get_institution_extra_context(self, extra_context):
        app_config = django_apps.get_app_config('edc_base')
        extra_context.update({
            'institution': app_config.institution,
            'copyright': app_config.copyright,
            'license': app_config.license or '',
            'disclaimer': app_config.disclaimer})
        return extra_context

    def add_view(self, request, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context = self.get_institution_extra_context(extra_context)
        return super().add_view(
            request, form_url=form_url, extra_context=extra_context)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context = self.get_institution_extra_context(extra_context)
        return super().change_view(
            request, object_id, form_url=form_url, extra_context=extra_context)


class ModelAdminRedirectMixin:

    """Redirect on add, change, or delete."""

    def redirect_url(self, request, obj, post_url_continue=None):
        return None

    def redirect_url_on_add(self, request, obj, post_url_continue=None):
        return self.redirect_url(request, obj, post_url_continue=post_url_continue)

    def redirect_url_on_change(self, request, obj, post_url_continue=None):
        return self.redirect_url(request, obj, post_url_continue=post_url_continue)

    def redirect_url_on_delete(self, request, obj_display, obj_id):
        return None

    def response_add(self, request, obj, post_url_continue=None):
        redirect_url = None
        if '_addanother' not in request.POST and '_continue' not in request.POST:
            redirect_url = self.redirect_url_on_add(request, obj)
        if redirect_url:
            return HttpResponseRedirect(redirect_url)
        return super().response_add(request, obj)

    def response_change(self, request, obj, post_url_continue=None):
        redirect_url = None
        if '_addanother' not in request.POST and '_continue' not in request.POST:
            redirect_url = self.redirect_url_on_change(request, obj)
        if redirect_url:
            return HttpResponseRedirect(redirect_url)
        return super().response_change(request, obj)

    def response_delete(self, request, obj_display, obj_id):
        redirect_url = self.redirect_url_on_delete(
            request, obj_display, obj_id)
        if redirect_url:
            return HttpResponseRedirect(redirect_url)
        return super().response_delete(request, obj_display, obj_id)


class ModelAdminNextUrlRedirectMixin(ModelAdminRedirectMixin):

    """Redirect on add, change, delete by reversing a url_name
    in the querystring.

    In your url &next=my_url_name,arg1,arg2&agr1=value1&arg2=
    value2&arg3=value3&arg4=value4...etc.
    """

    querystring_name = 'next'

    def render_delete_form(self, request, context):
        return super().render_delete_form(request, context)

    def delete_view(self, request, object_id, extra_context=None):
        return super().delete_view(request, object_id, extra_context=extra_context)

    def redirect_url(self, request, obj, post_url_continue=None):
        kwargs = request.GET.dict()
        redirect_url = super().redirect_url(
            request, obj, post_url_continue=post_url_continue)
        if kwargs.get(self.querystring_name):
            url_name = kwargs.get(self.querystring_name).split(',')[0]
            attrs = kwargs.get(self.querystring_name).split(',')[1:]
            kwargs = {k: kwargs.get(k) for k in attrs if kwargs.get(k)}
            redirect_url = reverse(url_name, kwargs=kwargs)
        return redirect_url


class ModelAdminModelRedirectMixin(ModelAdminRedirectMixin):

    """Redirect to another model's changelist on add, change or delete.
    """

    redirect_app_label = None
    redirect_model_name = None
    redirect_search_field = None
    redirect_namespace = 'admin'

    def search_value(self, obj):
        def objattr(inst):
            my_inst = inst
            for name in self.redirect_search_field.split('__'):
                my_inst = getattr(my_inst, name)
            return my_inst
        try:
            value = objattr(obj)
        except TypeError:
            value = None
        return value

    def redirect_url(self, request, obj, post_url_continue=None, namespace=None):
        namespace = namespace or self.redirect_namespace
        return '{}?q={}'.format(
            reverse(
                '{namespace}:{app_label}_{model_name}_changelist'.format(
                    namespace=namespace,
                    app_label=self.redirect_app_label,
                    model_name=self.redirect_model_name)),
            self.search_value(obj) or '')

    def redirect_url_on_delete(self, request, obj_display, obj_id, namespace=None):
        namespace = namespace or self.redirect_namespace
        return reverse(
            '{namespace}:{app_label}_{model_name}_changelist'.format(
                namespace=namespace,
                app_label=self.redirect_app_label,
                model_name=self.redirect_model_name))


class ModelAdminChangelistButtonMixin:

    changelist_model_button_template = (
        '<a href="{{url}}" class="button" title="{{title}}" {{disabled}}>{label}</a>')

    def button(self, url_name, reverse_args, disabled=None, label=None,
               title=None, namespace=None):
        label = label or 'change'
        if namespace:
            url_name = '{}:{}'.format(namespace, url_name)
        url = reverse(url_name, args=reverse_args)
        return self.button_template(label, url=url, disabled=disabled, title=title)

    def change_button(self, url_name, reverse_args, disabled=None,
                      label=None, title=None, namespace=None):
        label = label or 'change'
        if namespace:
            url_name = '{}:{}'.format(namespace, url_name)
        url = reverse(url_name, args=reverse_args)
        return self.button_template(label, url=url, disabled=disabled, title=title)

    def add_button(self, url_name, disabled=None, label=None,
                   querystring=None, namespace=None, title=None):
        label = label or 'add'
        if namespace:
            url_name = '{}:{}'.format(namespace, url_name)
        url = reverse(url_name) + '' if querystring is None else querystring
        return self.button_template(label, url=url, disabled=disabled, title=title)

    def button_template(self, label, disabled=None, title=None, url=None):
        title = title or ''
        disabled = 'disabled' if disabled else ''
        if disabled or not url:
            url = '#'
        button_template = self.changelist_model_button_template.format(
            label=label)
        button_template = format_html(
            button_template, disabled=disabled, title=title, url=url)
        return button_template


class ModelAdminChangelistModelButtonMixin(ModelAdminChangelistButtonMixin):

    """Use a button as a list_display field with a link to add,
    change or changelist.
    """

    def changelist_model_button(self, app_label, model_name, reverse_args=None,
                                namespace=None, change_label=None,
                                add_label=None, add_querystring=None,
                                disabled=None, title=None):
        if disabled:
            changelist_model_button = self.disabled_button(
                add_label or change_label)
        else:
            app_label = app_label
            model_name = model_name
            if reverse_args:
                changelist_model_button = self.change_model_button(
                    app_label, model_name, reverse_args, namespace=namespace,
                    label=change_label, title=title)
            else:
                changelist_model_button = self.add_model_button(
                    app_label, model_name, label=add_label,
                    querystring=add_querystring,
                    namespace=namespace, title=title)
        return changelist_model_button

    def change_model_button(self, app_label, model_name, reverse_args,
                            label=None, namespace=None, title=None):
        label = label or 'change'
        namespace = namespace or 'admin'
        url = reverse(
            '{namespace}:{app_label}_{model_name}_change'.format(
                namespace=namespace, app_label=app_label,
                model_name=model_name),
            args=reverse_args)
        return self.button_template(label, url=url, title=title)

    def add_model_button(self, app_label, model_name, label=None,
                         querystring=None, namespace=None, title=None):
        label = label or 'add'
        namespace = namespace or 'admin'
        url = reverse(
            ('{namespace}:{app_label}_{model_name}_add'.format(
                namespace=namespace, app_label=app_label, model_name=model_name))
            + (querystring or ''))
        return self.button_template(label, url=url, title=title)

    def changelist_list_button(self, app_label, model_name, querystring_value=None,
                               label=None, disabled=None, namespace=None, title=None):
        """Return a button that goes to the app changelist filter for
        this model instance.
        """
        label = label or 'change'
        namespace = namespace or 'admin'
        querystring = ''
        if querystring_value:
            querystring = '?q={}'.format(querystring_value)
        url = reverse(
            ('{namespace}:{app_label}_{model_name}_changelist'.format(
                namespace=namespace, app_label=app_label, model_name=model_name))
            + querystring)
        return self.button_template(label, disabled=disabled, title=title, url=url)

    def disabled_button(self, label):
        return self.button_template(label, disabled='disabled', url='#')


class ModelAdminFormInstructionsMixin:
    """Add instructions to the add view context.

    Override the change_form.html to add {{ instructions }}

    Create a blank change_form.html in your
    /templates/admin/<app_label> folder and add this
    (or something like it):

        {% extends "admin/change_form.html" %}
        {% block field_sets %}
        {% if instructions %}
            <p class="help"><b>Instructions:</b>&nbsp;{{ instructions }}</p>
        {% endif %}
        {% if additional_instructions %}
            <p class="help"><b>Additional Instructions:</b>
            &nbsp;{{ additional_instructions }}</p>
        {% endif %}
        {{ block.super }}
        {% endblock %}
    """

    instructions = (
        'Please complete the form below. '
        'Required questions are in bold. '
        'When all required questions are complete click SAVE '
        'or, if available, SAVE NEXT. Based on your responses, '
        'additional questions may be '
        'required or some answers may need to be corrected.')

    additional_instructions = None

    add_additional_instructions = None
    add_instructions = None

    change_additional_instructions = None
    change_instructions = None

    def update_add_instructions(self, extra_context):
        extra_context = extra_context or {}
        extra_context[
            'instructions'] = self.add_instructions or self.instructions
        extra_context['additional_instructions'] = (
            self.add_additional_instructions or self.additional_instructions)
        return extra_context

    def update_change_instructions(self, extra_context):
        extra_context = extra_context or {}
        extra_context[
            'instructions'] = self.change_instructions or self.instructions
        extra_context['additional_instructions'] = (
            self.change_additional_instructions or self.additional_instructions)
        return extra_context

    def add_view(self, request, form_url='', extra_context=None):
        extra_context = self.update_add_instructions(extra_context)
        return super(ModelAdminFormInstructionsMixin, self).add_view(
            request, form_url=form_url, extra_context=extra_context)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = self.update_change_instructions(extra_context)
        return super(ModelAdminFormInstructionsMixin, self).change_view(
            request, object_id, form_url=form_url, extra_context=extra_context)


class ModelAdminAuditFieldsMixin:

    def save_model(self, request, obj, form, change):
        if not change:
            obj.user_created = request.user.username
            obj.created = get_utcnow()
        else:
            obj.user_modified = request.user.username
            obj.modified = get_utcnow()
        super(ModelAdminAuditFieldsMixin, self).save_model(
            request, obj, form, change)

    def get_list_filter(self, request):
        columns = ['created', 'modified', 'user_created',
                   'user_modified', 'hostname_created', 'hostname_modified']
        self.list_filter = list(self.list_filter or [])
        self.list_filter = self.list_filter + \
            [item for item in columns if item not in self.list_filter]
        return tuple(self.list_filter)

    def get_readonly_fields(self, request, obj=None):
        # FIXME: somewhere the readonly_fields is being changed to a list
        readonly_fields = super().get_readonly_fields(request, obj=obj)
        if readonly_fields:
            readonly_fields = tuple(readonly_fields)
        return readonly_fields + audit_fields


class ModelAdminFormAutoNumberMixin:

    def auto_number(self, form):
        WIDGET = 1
        auto_number = True
        if 'auto_number' in dir(form._meta):
            auto_number = form._meta.auto_number
        if auto_number:
            for index, fld in enumerate(form.base_fields.items()):
                if not re.match(r'^\d+\.', str(fld[WIDGET].label)):
                    fld[WIDGET].label = mark_safe(
                        '<a title="{0}">{1}</a>. {2}'.format(
                            fld[0], str(index + 1), str(fld[WIDGET].label)))
        return form

    def get_form(self, request, obj=None, **kwargs):
        form = super(ModelAdminFormAutoNumberMixin, self).get_form(
            request, obj, **kwargs)
        form = self.auto_number(form)
        return form


class StackedInlineMixin(ModelAdminAuditFieldsMixin):
    pass


class TabularInlineMixin(ModelAdminAuditFieldsMixin):
    pass


class LimitedAdminInlineMixin:
    """Limit choices on a foreignkey field in an inline to a value
    on the parent model.

    From getresults_csv. For example, model CsvDictionary is an
    inline to CsvFormat. The inline has a foreignkey to model
    CsvFields. By using the mixin, csv_field is filtered by the
    value of csv_format instead of showing everything in CsvFields.

        class CsvDictionaryInline(LimitedAdminInlineMixin,
                                  admin.TabularInline):
            model = CsvDictionary
            form = CsvDictionaryForm
            extra = 0

            def get_filters(self, obj):
                if obj:
                    return (('csv_field', dict(csv_format=obj.id)),)
                else:
                    return ()

        class CsvFormatAdmin(admin.ModelAdmin):
            inlines = [CsvDictionaryInline]
        admin_site.register(CsvFormat, CsvFormatAdmin)
    """

    @staticmethod
    def limit_inline_choices(formset, field, empty=False, **filters):
        assert field in formset.form.base_fields
        qs = formset.form.base_fields[field].queryset
        if empty:
            formset.form.base_fields[field].queryset = qs.none()
        else:
            qs = qs.filter(**filters)
            formset.form.base_fields[field].queryset = qs

    def get_formset(self, request, obj=None, **kwargs):
        formset = super(LimitedAdminInlineMixin, self).get_formset(
            request, obj, **kwargs)

        for (field, filters) in self.get_filters(obj):
            if obj:
                self.limit_inline_choices(formset, field, **filters)
            else:
                self.limit_inline_choices(formset, field, empty=True)

        return formset

    def get_filters(self, obj):
        return getattr(self, 'filters', ())


class ModelAdminReadOnlyMixin:
    """
    A mixin that presents an admin form with the submit_row replaced
    with a Close button effectively making the form a read-only form.

        The Close button navigates to the "next" url from the
        GET/querystring.

        Subclass the change_form.html. Add

            {% block submit_buttons_bottom %}
            {% if edc_readonly %}
              <div class="submit_row"><input type="button"
              value="Close" class="default" name="_close"
              onclick="location.href='{{ edc_readonly_next }}';" />
              </div>
            {% else %}
              {% submit_row %}
            {% endif %}
            {% endblock %}

        to the admin url querystring add "next" and "edc_readonly=1"

    """

    querystring_name = 'next'

    def get_form(self, request, obj=None, **kwargs):
        form = super(ModelAdminReadOnlyMixin, self).get_form(
            request, obj, **kwargs)
        if request.GET.get('edc_readonly'):
            for form_field in form.base_fields.values():
                form_field.disabled = True
                try:
                    form_field.widget.can_add_related = False
                    form_field.widget.can_change_related = False
                    form_field.widget.can_delete_related = False
                except AttributeError:
                    pass
                if isinstance(form_field.widget, AdminDateWidget):
                    form_field.widget = DateInput()
        return form

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        if request.GET.get('edc_readonly'):
            extra_context.update(
                {'edc_readonly': request.GET.get('edc_readonly')})
            extra_context.update(
                {'edc_readonly_next': request.GET.get(self.querystring_name)})
        return super(ModelAdminReadOnlyMixin, self).change_view(
            request, object_id, form_url=form_url, extra_context=extra_context)
