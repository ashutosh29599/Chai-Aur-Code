from django import forms
from django.db import models
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


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    bio = models.TextField(max_length=240)

    def __str__(self) -> str:
        return self.user.username

class UserProfileUpdateForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "First Name"}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Last Name"}))
    email = forms.EmailField(widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Email"}))
    bio = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5, "placeholder": "Write a few words about yourself..."}))

    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'email', 'bio']
