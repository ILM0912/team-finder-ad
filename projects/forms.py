from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()


class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('name', 'surname', 'email', 'password')
        widgets = {'password': forms.PasswordInput()}


class LoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput()
    )
    password = forms.CharField(
        widget=forms.PasswordInput()
    )


class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(
        widget=forms.PasswordInput()
    )
    new_password1 = forms.CharField(
        widget=forms.PasswordInput()
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput()
    )