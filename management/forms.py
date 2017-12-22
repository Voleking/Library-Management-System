from django import froms
from .models import *

class CategorySelectForm(froms.Form):
    category = forms.ModelChoiceField(queryset=BookCategory.objects.all(),
    )

class StateSelectForm(forms.Form):
    states = forms.ChoiceField(
        choices=us_states(),
        widget=forms.Select(attrs={'class': 'form-control'})
    )
