from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


class RegistrationForm(UserCreationForm):
    first_name = forms.CharField(
        label="First Name",
        label_suffix="",
        max_length=150,
        widget=forms.TextInput(
            attrs={
                "title": "First Name",
                "placeholder": "Enter First Name",
                "class": "form-control",
            }
        ),
    )
    last_name = forms.CharField(
        label="Last Name",
        label_suffix="",
        max_length=150,
        widget=forms.TextInput(
            attrs={
                "title": "Last Name",
                "placeholder": "Enter Last Name",
                "class": "form-control",
            }
        ),
    )
    username = forms.CharField(
        label="Username",
        label_suffix="",
        max_length=150,
        widget=forms.TextInput(
            attrs={
                "title": "Username",
                "placeholder": "Enter Username",
                "class": "form-control",
            }
        ),
    )
    email = forms.EmailField(
        label="Email Address",
        label_suffix="",
        max_length=150,
        widget=forms.EmailInput(
            attrs={
                "title": "Email Address",
                "placeholder": "Enter Email Address",
                "class": "form-control",
            }
        ),
    )
    password1 = forms.CharField(
        label="Password",
        label_suffix="",
        max_length=150,
        widget=forms.PasswordInput(
            attrs={
                "title": "Password",
                "placeholder": "Enter Password",
                "class": "form-control",
            }
        ),
    )
    password2 = forms.CharField(
        label="Confirm Password",
        label_suffix="",
        max_length=150,
        widget=forms.PasswordInput(
            attrs={
                "title": "Confirm Password",
                "placeholder": "Confirm Password",
                "class": "form-control",
            }
        ),
    )

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "username",
            "email",
            "password1",
            "password2",
        )


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Username",
        max_length=150,
        label_suffix="",
        widget=forms.TextInput(
            attrs={
                "title": "Username",
                "placeholder": "Enter Username",
                "class": "form-control",
            }
        ),
    )
    password = forms.CharField(
        label="Password",
        label_suffix="",
        widget=forms.PasswordInput(
            attrs={
                "title": "Password",
                "placeholder": "Enter Password",
                "class": "form-control",
            }
        ),
    )
