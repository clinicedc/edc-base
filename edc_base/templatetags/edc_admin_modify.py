from django import template
from django.contrib.admin.templatetags.admin_modify import submit_row as original_submit_row

register = template.Library()


@register.inclusion_tag('admin/submit_line.html', takes_context=True)
def edc_submit_row(context):
    try:
        ctx = original_submit_row(context)
    except KeyError:
        ctx = {'add': True}
    is_popup = context.get('is_popup', False)
    request = context.get('request', None)
    show = request.GET.get('show') == 'forms'
    ctx.update({
        'show_savenext': (not is_popup and context.get('add') and show)
    })
    return ctx
