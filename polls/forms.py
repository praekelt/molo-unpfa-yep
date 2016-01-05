from django import forms
from models import Choice


class TextVoteForm(forms.Form):
    answer = forms.CharField(required=True)


class VoteForm(forms.Form):
    choice = forms.MultipleChoiceField(required=True)

    def __init__(self, *args, **kwargs):
        super(VoteForm, self).__init__(*args, **kwargs)
        self.fields['choice'].choices = [(
            c.pk, c.title) for c in Choice.objects.all()]

    def clean_choice(self):
        return self.cleaned_data['choice']
