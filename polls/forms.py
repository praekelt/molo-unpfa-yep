from django import forms


class TextVoteForm(forms.Form):
    answer = forms.CharField(required=True)


class VoteForm(forms.Form):
    choice = forms.IntegerField(required=True)
