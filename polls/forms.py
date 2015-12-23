from django import forms


class TextVoteForm(forms.Form):
    answer = forms.CharField(required=True)
