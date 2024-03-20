from Users.models import CustomUser
from django import forms


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="Confirm password", required=True)
    birthday = forms.DateField(required=True,
                               widget=forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
                               input_formats=["%Y-%m-%d"]
                               )
    first_name = forms.CharField(required=True)

    class Meta:
        model = CustomUser
        fields = ('username', 'password', 'confirm_password', 'first_name', 'last_name', 'birthday', 'gender',
                  'phone_number', 'email')


class LoginForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['username', 'password']
