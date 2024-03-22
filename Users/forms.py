from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm

from Users.models import CustomUser


class RegisterForm(UserCreationForm):
    birthday = forms.DateField(required=True,
                               widget=forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
                               input_formats=["%Y-%m-%d"]
                               )
    first_name = forms.CharField(required=True)

    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'birthday', 'gender',
                  'phone_number', 'email')

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirmation = cleaned_data.get('confirm_password')
        if password != password_confirmation:
            raise forms.ValidationError('Passwords must match.')
        return cleaned_data


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email', 'birthday', 'gender', 'phone_number')
