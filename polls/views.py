from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic
from django.utils.translation import ugettext_lazy as _
from polls.models import Choice, Question, PollVote
from django.db.models import F


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
    total_votes = sum(c.vote_count for c in choices)
    choice_color = ['orange', 'purple', 'turq']
    index = 0
    for choice in choices:
        if index >= len(choice_color):
            index = 0
        vote_percentage = int(choice.vote_count * 100.0 / total_votes)
        choice.percentage = vote_percentage
        choice.color = choice_color[index]
        index += 1

    context = {
        'question': question,
        'total': total_votes,
        'choices': sorted(choices, key=lambda x: x.percentage, reverse=True)
    }
    return render(request, 'polls/results.html', context,)


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = Choice.objects.filter(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': _("You didn't select a choice."),
        })
    else:
        selected_choice.update(vote_count=F('vote_count') + 1)
        PollVote.objects.create(user=request.user,
                                choice=selected_choice[0],
                                question=question)
        return HttpResponseRedirect(reverse('molo.polls:results',
                                            args=(question.id,)))
