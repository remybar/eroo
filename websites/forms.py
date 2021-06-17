from django import forms

class GenerateForm(forms.Form):
    rental_url = forms.URLField()
