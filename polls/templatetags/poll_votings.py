
from copy import copy

from django import template

from polls.models import Question

register = template.Library()


@register.inclusion_tag('polls/poll_page.html',
                        takes_context=True)
def poll_page(context, pk=None, page=None):
    context = copy(context)
    context.update({
        'questions': Question.objects.live().child_of(page)
        if page else Question.objects.none()
    })
    return context


@register.assignment_tag(takes_context=True)
def can_vote(context, question):
    request = context['request']
    return question.can_vote(request.user)


@register.assignment_tag(takes_context=True)
def user_choice(context, question):
    request = context['request']
    return question.user_choice(request.user)
