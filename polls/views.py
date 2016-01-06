from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic
from django.utils.translation import ugettext_lazy as _
from polls.models import (Choice, Question, FreeTextVote, ChoiceVote,
                          FreeTextQuestion)
from django .db.models import F
from django.views.generic.edit import FormView
from forms import TextVoteForm
from django.contrib.auth.decorators import login_required
import numbers


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'


def poll_results(request, poll_id):
    question = get_object_or_404(Question, pk=poll_id)
    choices = list(question.choices())
    total_votes = sum(c.votes for c in choices)
    choice_color = ['orange', 'purple', 'turq']
    index = 0
    for choice in choices:
        vote_percentage = 0
        if index >= len(choice_color):
            index = 0
        if choice.votes > 0:
            vote_percentage = int(choice.votes * 100.0 / total_votes)
        choice.percentage = vote_percentage
        choice.color = choice_color[index]
        index += 1

    context = {
        'question': question,
        'total': total_votes,
        'choices': sorted(choices, key=lambda x: x.percentage, reverse=True)
    }
    return render(request, 'polls/results.html', context,)


@login_required
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = Choice.objects.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': _("You didn't select a choice."),
        })
    else:
        obj, created = ChoiceVote.objects.get_or_create(
            user=request.user,
            question=question)
        if created:
            selected_choice = request.POST.getlist('choice')
            for choice in selected_choice:
                choice = Choice.objects.get(pk=choice)
                obj.choice.add(choice)
                choice.votes = F('votes') + 1
                choice.choice_votes.add(obj)
                choice.save()
            return HttpResponseRedirect(reverse('molo.polls:results',
                                                args=(question.id,)))
        else:
            return render(request, 'polls/detail.html', {
                'question': question,
                'error_message': _("You are only allowed to vote once."),
            })


class FreeTextVoteView(FormView):
    form_class = TextVoteForm
    template_name = 'polls/free_text_detail.html'

    def get_context_data(self, *args, **kwargs):
        context = super(
            FreeTextVoteView, self).get_context_data(*args, **kwargs)
        question_id = self.kwargs.get('question_id')
        question = get_object_or_404(Question, pk=question_id)
        context.update({'question': question})
        return context

    def form_valid(self, form, *args, **kwargs):
        question_id = self.kwargs.get('question_id')
        question = get_object_or_404(FreeTextQuestion, pk=question_id)
        if question.numerical and isinstance(
                form.cleaned_data['answer'], numbers.Number) is False:
                    raise ValidationError(
                        _('Invalid value: %(value)s'),
                        code='invalid',)
        FreeTextVote.objects.get_or_create(
            user=self.request.user,
            question=question,
            defaults={
                'answer': form.cleaned_data['answer']
            })

        return HttpResponseRedirect(
            reverse('molo.polls:results', args=(question.id, {'error_message': _("You are only allowed to vote once."}))))
