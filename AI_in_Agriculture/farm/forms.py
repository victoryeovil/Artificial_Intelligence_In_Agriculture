from django import forms

class FarmerInputForm(forms.Form):
    nutrient_1 = forms.FloatField()
    nutrient_2 = forms.FloatField()
    nutrient_3 = forms.FloatField()
