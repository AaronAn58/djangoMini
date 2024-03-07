from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm

from .models import CustomUser


class RegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'age', 'phone', 'address', 'password1', 'password2']


class UpdateUserInfoForm(ModelForm):
    email = forms.EmailField()

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'age', 'phone', 'address']

    # def __init__(self, *args, **kwargs):
    #     super(UpdateUserInfoForm, self).__init__(*args, **kwargs)
    #     # Exclude password field
    #     self.fields.pop('password')
