import re

from django.http.response import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.utils.html import format_html
from django.utils import timezone


class ModelAdminRedirectMixin(object):

    def redirect_url(self, request, obj, post_url_continue=None):
        return None

    def redirect_url_on_add(self, request, obj, post_url_continue=None):
        return self.redirect_url(request, obj, post_url_continue)

    def redirect_url_on_change(self, request, obj, post_url_continue=None):
        return self.redirect_url(request, obj, post_url_continue)

    def redirect_url_on_delete(self, request, obj_display, obj_id):
        return None

    def response_add(self, request, obj, post_url_continue=None):
        redirect_url = None
        if '_addanother' not in request.POST and '_continue' not in request.POST:
            redirect_url = self.redirect_url_on_add(request, obj)
        if redirect_url:
            return HttpResponseRedirect(redirect_url)
        return super(ModelAdminRedirectMixin, self).response_add(request, obj)

    def response_change(self, request, obj, post_url_continue=None):
        redirect_url = None
        if '_addanother' not in request.POST and '_continue' not in request.POST:
            redirect_url = self.redirect_url_on_change(request, obj)
        if redirect_url:
            return HttpResponseRedirect(redirect_url)
        return super(ModelAdminRedirectMixin, self).response_change(request, obj)

    def response_delete(self, request, obj_display, obj_id):
        redirect_url = self.redirect_url_on_delete(request, obj_display, obj_id)
        if redirect_url:
            return HttpResponseRedirect(redirect_url)
        return super(ModelAdminRedirectMixin, self).response_delete(request, obj_display, obj_id)


class ModelAdminModelRedirectMixin(ModelAdminRedirectMixin):

    redirect_app_label = None
    redirect_model_name = None
    redirect_search_field = None

    def search_value(self, obj):
        def objattr(inst):
            my_inst = inst
            for name in self.redirect_search_field.split('.'):
                my_inst = getattr(my_inst, name)
            return my_inst
        try:
            value = objattr(obj)
        except TypeError:
            value = None
        return value

    def redirect_url(self, request, obj, post_url_continue=None):
        return '{}?q={}'.format(
            reverse(
                'admin:{app_label}_{model_name}_changelist'.format(
                    app_label=self.redirect_app_label, model_name=self.redirect_model_name)),
            self.search_value(obj) or '')

    def redirect_url_on_delete(self, request, obj_display, obj_id):
        return reverse(
            'admin:{app_label}_{model_name}_changelist'.format(
                app_label=self.redirect_app_label, model_name=self.redirect_model_name))


class ModelAdminChangelistModelButtonMixin(object):

    changelist_model_button_template = '<a href="{{}}" class="button" {}>{}</a>'

    def changelist_model_button(self, app_label, model_name, reverse_args=None, change_label=None,
                                add_label=None, add_querystring=None, disabled=None):
        if disabled:
            changelist_model_button = self.disabled_button(add_label or change_label)
        else:
            app_label = app_label
            model_name = model_name
            if reverse_args:
                enabled_button = self.change_button(
                    app_label, model_name, reverse_args, label=change_label)
            else:
                enabled_button = self.add_button(app_label, model_name, add_label, add_querystring)
            changelist_model_button = enabled_button or self.button_template(disabled=True)
        return changelist_model_button

    def change_button(self, app_label, model_name, reverse_args, label=None):
        label = label or 'change'
        return format_html(
            self.button_template(label),
            reverse(
                'admin:{app_label}_{model_name}_change'.format(app_label=app_label, model_name=model_name),
                args=reverse_args))

    def add_button(self, app_label, model_name, label=None, querystring=None):
        label = label or 'add'
        return format_html(
            self.button_template(label),
            reverse(
                'admin:{app_label}_{model_name}_add'.format(
                    app_label=app_label, model_name=model_name)) + (querystring or ''))

    def disabled_button(self, label):
        return self.changelist_model_button_template.format('disabled', label).format('#')

    def changelist_list_button(self, app_label, model_name, querystring_value=None,
                               label=None, disabled=None):
        label = label or 'change'
        querystring = ''
        if querystring_value:
            querystring = '?q={}'.format(querystring_value)
        return format_html(
            self.button_template(label, disabled),
            reverse(
                'admin:{app_label}_{model_name}_changelist'.format(
                    app_label=app_label, model_name=model_name)) + querystring)

    def button_template(self, label, disabled=None):
        disabled = 'disabled' if disabled else ''
        return self.changelist_model_button_template.format(disabled, label)


class ModelAdminFormInstructionsMixin(object):
    """Add instructions to the add view context.

    Override the change_form.html to add {{ instructions }}

    Create a blank change_form.html in your /templates/admin/<app_label> folder
    and add this (or something like it):

        {% extends "admin/change_form.html" %}
        {% block field_sets %}
        {% if instructions %}
            <p class="help"><b>Instructions:</b>&nbsp;{{ instructions }}</p>
        {% endif %}
        {% if additional_instructions %}
            <p class="help"><b>Additional Instructions:</b>&nbsp;{{ additional_instructions }}</p>
        {% endif %}
        {{ block.super }}
        {% endblock %}

    """

    instructions = (
        'Please complete the form below. '
        'Required questions are in bold. '
        'When all required questions are complete click SAVE '
        'or, if available, SAVE NEXT. Based on your responses, additional questions may be '
        'required or some answers may need to be corrected.')

    additional_instructions = None

    add_additional_instructions = None
    add_instructions = None

    change_additional_instructions = None
    change_instructions = None

    def update_add_instructions(self, extra_context):
        extra_context = extra_context or {}
        extra_context['instructions'] = self.add_instructions or self.instructions
        extra_context['additional_instructions'] = (
            self.add_additional_instructions or self.additional_instructions)
        return extra_context

    def update_change_instructions(self, extra_context):
        extra_context = extra_context or {}
        extra_context['instructions'] = self.change_instructions or self.instructions
        extra_context['additional_instructions'] = (
            self.change_additional_instructions or self.additional_instructions)
        return extra_context

    def add_view(self, request, form_url='', extra_context=None):
        extra_context = self.update_add_instructions(extra_context)
        print(extra_context)
        print(self.instructions)
        return super(ModelAdminFormInstructionsMixin, self).add_view(
            request, form_url=form_url, extra_context=extra_context)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = self.update_change_instructions(extra_context)
        return super(ModelAdminFormInstructionsMixin, self).change_view(
            request, object_id, form_url=form_url, extra_context=extra_context)


class ModelAdminAuditFieldsMixin(object):

    def save_model(self, request, obj, form, change):
        if not change:
            obj.user_created = request.user.username
            obj.created = timezone.now()
        else:
            obj.user_modified = request.user.username
            obj.modified = timezone.now()
        super(ModelAdminAuditFieldsMixin, self).save_model(request, obj, form, change)

    def get_list_filter(self, request):
        columns = ['created', 'modified', 'user_created', 'user_modified', 'hostname_created']
        self.list_filter = list(self.list_filter or [])
        self.list_filter = self.list_filter + [item for item in columns if item not in self.list_filter]
        return tuple(self.list_filter)


class ModelAdminFormAutoNumberMixin(object):

    def auto_number(self, form):
        WIDGET = 1
        auto_number = True
        if 'auto_number' in dir(form._meta):
            auto_number = form._meta.auto_number
        if auto_number:
            for index, fld in enumerate(form.base_fields.items()):
                if not re.match(r'^\d+\.', str(fld[WIDGET].label)):
                    fld[WIDGET].label = '{0}. {1}'.format(str(index + 1), str(fld[WIDGET].label))
        return form

    def get_form(self, request, obj=None, **kwargs):
        form = super(ModelAdminFormAutoNumberMixin, self).get_form(request, obj, **kwargs)
        form = self.auto_number(form)
        return form
