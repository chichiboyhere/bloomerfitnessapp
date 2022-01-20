from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class NewUserCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('email','first_name', 'last_name', 'weight', 'height', 'waist', 'hips','gender')


class NewUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('weight', 'height','waist', 'hips')
        weight = forms.DecimalField(
            
            widget=forms.NumberInput(attrs={
                "class": "form-control"
            })
        )
        height = forms.DecimalField(
            
            widget=forms.NumberInput(attrs={
                "class": "form-control"
            })
        )
        waist = forms.DecimalField(
            
            widget=forms.NumberInput(attrs={
                "class": "form-control"
            })
        )
        hips = forms.DecimalField(
            
            widget=forms.NumberInput(attrs={
                "class": "form-control"
            })
        )
   
class WeightTrackForm(forms.Form):
    desired_weight=forms.DecimalField(
            max_digits=5, decimal_places=2,
            widget=forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "Desired Weight in Kg",   
            })
    )   


class AuthenticationForm(forms.Form):
    email= forms.CharField(max_length=64)
    password = forms.CharField(widget=forms.PasswordInput())

class FitnessMeterForm(forms.Form):
	name = forms.CharField(max_length=50, required=False)
	weight=forms.DecimalField(max_digits=5, decimal_places=2)
	WEIGHT_UNITS= [
    ('kg', 'Kg'),
    ('lbs', 'Lbs')
    ]
	weightunit=forms.CharField(widget=forms.Select(choices=WEIGHT_UNITS))
	height=forms.DecimalField(max_digits=5, decimal_places=2)
	waist =forms.DecimalField(max_digits=5, decimal_places=2)
	hips =forms.DecimalField(max_digits=5, decimal_places=2)
	GENDER=(
		('female', 'Female'),
        ('male', 'Male'),
	)
	gender = forms.ChoiceField(choices=GENDER)

class WeightMetricForm(forms.Form):
    weight = forms.DecimalField(
            max_digits=5, decimal_places=2,
            widget=forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "Weight in Pounds",
                
            })
        )
class HeightMetricForm(forms.Form):        
    height = forms.DecimalField(
            max_digits=5, decimal_places=2,
            widget=forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "feet",
            })
        )
    height2 = forms.DecimalField(
            max_digits=5, decimal_places=2,
            widget=forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "inches",
                'required': False,
            })
        )    
        
class ContactForm(forms.Form):
    author = forms.CharField(
        max_length=60,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Your Name"
        })
    )
    email = forms.EmailField(
        max_length=60,
        widget=forms.EmailInput(attrs={
            "class": "form-control",
            "placeholder": "Email Address"
        })
    )
    body = forms.CharField(widget=forms.Textarea(
        attrs={
            "class": "form-control",
            "placeholder": "Message"
        })
    )