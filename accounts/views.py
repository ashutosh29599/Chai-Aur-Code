from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm

from profiles.models import Profile
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
            return redirect("tweet_home")
    else:
        form = UserRegistrationForm()

    return render(request, "registration/register.html", {"form": form})


@login_required
def change_password(request):
    if request.method == "POST":
        form = PasswordChangeForm(user=request.user, data=request.POST)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)

        return redirect(reverse("profile", kwargs={"user_id": request.user.id}))
    
    form = PasswordChangeForm(request.user)
    return render(request, "change_password/change_password.html", {"form": form})
