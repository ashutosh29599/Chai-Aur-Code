from django.shortcuts import render, redirect
from django.contrib.auth import login

from tweet.models import Profile
from .forms import UserRegistrationForm

# Create your views here.

def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password1"])
            user.save()

            Profile.objects.create(user=user, email=user.email)

            login(request, user)
            return redirect("tweet_list")
    else:
        form = UserRegistrationForm()

    return render(request, "registration/register.html", {"form": form})
