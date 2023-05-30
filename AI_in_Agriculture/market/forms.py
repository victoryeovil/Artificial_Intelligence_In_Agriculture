from django import forms
from .models import Product, Farmer
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class ProductForm(forms.ModelForm):
	class Meta:
		model = Product
		fields = ['name', 'description', 'price', 'image']
		widgets = {
			'description': forms.Textarea(attrs={'rows': 5}),
		}

class FarmerForm(forms.ModelForm):
	class Meta:
		model = Farmer
		fields = ['location', 'latitude', 'longitude']
		



class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, required=True, help_text='Required')
    first_name = forms.CharField(max_length=30, required=True, help_text='Required')
    last_name = forms.CharField(max_length=30, required=True, help_text='Required')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

