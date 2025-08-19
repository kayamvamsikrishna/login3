from app1.models import *
from django import forms

class UserForm(forms.ModelForm):
    class Meta:
        model=User
        #fields='__all__'
        fields=['username','email','password']
        widgets={'password':forms.PasswordInput}

class ProfileForm(forms.ModelForm):
    class Meta:
        model=Profile
        #fields='__all__'
        fields=['address','profile_pic']