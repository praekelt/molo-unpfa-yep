
from copy import copy

from django import template

from surveys.models import Survey

register = template.Library()


@register.inclusion_tag('surveys/survey_page.html',
                        takes_context=True)
def survey_page(context, pk=None, page=None):
    context = copy(context)
    survey_questions = Survey.objects.filter(page=page.id)
    context.update({
        'questions': survey_questions
    })
    return context
