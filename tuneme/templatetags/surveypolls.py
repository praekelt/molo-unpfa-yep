from django import template
from django.forms.fields import CheckboxInput

register = template.Library()


@register.assignment_tag
def get_surveytype():
    return "surveys"


@register.assignment_tag
def get_pollstype():
    return "polls"


@register.assignment_tag
def get_competitiontype():
    return "competition"


@register.filter(name='is_checkbox')
def is_checkbox(value):
    return isinstance(value, CheckboxInput)
