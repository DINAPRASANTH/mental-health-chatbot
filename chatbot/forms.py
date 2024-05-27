from django import forms

class PreferenceForm(forms.Form):
    pet = forms.CharField()
    color = forms.CharField()
    season = forms.CharField()
    gender = forms.CharField()
    age = forms.CharField()
