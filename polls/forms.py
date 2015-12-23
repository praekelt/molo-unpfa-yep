from django import forms


class TextVoteForm(forms.Form):
    answer = forms.TextField(required=True)


class VoteForm(forms.Form):
    choice = forms.TextField(required=True)
