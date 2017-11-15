
class ModelAdminFormInstructionsMixin:
    """Add instructions to the add view context.

    Override the change_form.html to add {{ instructions }}

    Create a blank change_form.html in your
    /templates/admin/<app_label> folder and add this
    (or something like it):

        {% extends "admin/change_form.html" %}
        {% block field_sets %}
        {% if instructions %}
            <H5>Instructions:</H5><p>{{ instructions }}</p>
        {% endif %}
        {% if additional_instructions %}
            <H5>Additional Instructions:</H5><p>{{ additional_instructions }}</p>
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
        return super().add_view(
            request, form_url=form_url, extra_context=extra_context)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = self.update_change_instructions(extra_context)
        return super().change_view(
            request, object_id, form_url=form_url, extra_context=extra_context)
