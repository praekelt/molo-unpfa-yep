from django import forms
from datetime import datetime
from django.forms.extras.widgets import SelectDateWidget

from molo.profiles.forms import DateOfBirthForm


class DateOfBirthForm(DateOfBirthForm):
    date_of_birth = forms.DateField(
        widget=SelectDateWidget(
            years=list(reversed([y for y in range(1930, datetime.now().year)]))
        ), initial=lambda: datetime(datetime.today().year - 25, 1, 1)
    )
