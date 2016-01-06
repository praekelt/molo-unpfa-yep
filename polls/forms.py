from django import forms
from models import Choice
from django.utils.translation import ugettext_lazy as _
import numbers
from django.core.exceptions import ValidationError


class TextVoteForm(forms.Form):
    answer = forms.CharField(required=True)


class NumericalTextVoteForm(forms.Form):
    answer = forms.IntegerField(required=True)

    def clean_answer(self):
        selected_answer = self.cleaned_data['answer']
        if not isinstance(selected_answer, numbers.Number):
            raise ValidationError(
                _("You did not enter a numerical value. Please try again."))
        return selected_answer


class VoteForm(forms.Form):
    choice = forms.MultipleChoiceField(
        required=True,
        error_messages={'required': _("You didn't select a choice")})

    def __init__(self, *args, **kwargs):
        super(VoteForm, self).__init__(*args, **kwargs)
        self.fields['choice'].choices = [(
            c.pk, c.title) for c in Choice.objects.all()]
