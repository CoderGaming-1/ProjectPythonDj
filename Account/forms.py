from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Users
class LoginForm(forms.Form):
    email = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    password = forms.CharField(
        widget= forms.TextInput(
            attrs= {
                "class": "form-control"
            }
        )
    )

class SignUpForm(UserCreationForm):
    email = forms.CharField(
        widget= forms.TextInput(
            attrs= {
                "class": "form-control"
            }
        )
    )
    
    password1 = forms.CharField(
        widget= forms.TextInput(
            attrs= {
                "class": "form-control"
            }
        )
    )
    
    class Meta:
        model = Users
        fields = ('email','password1','password2')
class PasswordResetForm(forms.Form):
    email = forms.EmailField(max_length=254, required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))