from django import forms
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .models import Tweet, Profile


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

class UserProfileUpdateForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "First Name"}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Last Name"}))
    email = forms.EmailField(widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Email"}))
    bio = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5, "placeholder": "Write a few words about yourself..."}))

    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'email', 'bio']

    def __init__(self, *args, **kwargs):
        first_name = kwargs.pop('first_name', None)
        last_name = kwargs.pop('last_name', None)
        email = kwargs.pop('email', None)
        bio = kwargs.pop('bio', None)
        
        super(UserProfileUpdateForm, self).__init__(*args, **kwargs)

        if first_name:
            self.fields['first_name'].widget.attrs.update({'placeholder': first_name, 'class': 'form-control'})
        if last_name:
            self.fields['last_name'].widget.attrs.update({'placeholder': last_name, 'class': 'form-control'})
        if email:
            self.fields['email'].widget.attrs.update({'placeholder': email, 'class': 'form-control'})
        if bio:
            self.fields['bio'].widget.attrs.update({'placeholder': bio, 'class': 'form-control'})

