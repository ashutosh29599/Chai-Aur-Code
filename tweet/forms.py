from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .models import Tweet


class TweetForm(forms.ModelForm):
    class Meta:
        model = Tweet
        fields = ["text", "photo"]  # this is a list -- we are using a model made by us.


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "password1",
            "password2",
        )  # this is a tuple -- we are using a built-in model.
