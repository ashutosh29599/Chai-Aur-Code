from django import forms
from django.db import models
from django.contrib.auth.models import User

from .models import Tweet


class TweetForm(forms.ModelForm):
    class Meta:
        model = Tweet
        fields = ["text", "photo"]  # this is a list -- we are using a model made by us.
