from django import template

register = template.Library()


@register.assignment_tag
def get_surveytype():
    return "surveys"


@register.assignment_tag
def get_pollstype():
    return "polls"
