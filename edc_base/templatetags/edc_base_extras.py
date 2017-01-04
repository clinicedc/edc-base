from django import template

from ..exceptions import AgeValueError
from ..utils import age

register = template.Library()


@register.simple_tag(takes_context=True)
def age_in_years(context, born):
    age_in_years = None
    try:
        age_in_years = age(born, context.get('reference_datetime')).years
    except AgeValueError:
        age_in_years = None
    return age_in_years or born
