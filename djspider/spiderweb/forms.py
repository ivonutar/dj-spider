from django import forms


class TargetForm(forms.Form):
    url = forms.CharField(label='URL', max_length=200)
