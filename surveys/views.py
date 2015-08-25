from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.views import generic
from django.utils.translation import ugettext_lazy as _
from surveys.models import Answer, Survey


class DetailView(generic.DetailView):
    model = Survey
    template_name = 'surveys/detail.html'


def survey(request, question_id):
    question = get_object_or_404(Survey, pk=question_id)
    answer = request.POST['answer']
    if answer:
        answer_obj = Answer(survey=question, answer_text=answer)
        answer_obj.save()
        return HttpResponseRedirect(request.site.root_page.url)
    else:
        return render(request, 'surveys/detail.html', {
            'question': question,
            'error_message': _("You didn't enter the answer."),
        })
