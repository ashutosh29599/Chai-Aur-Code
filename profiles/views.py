from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from django.urls import reverse

from .models import Profile
from .forms import UserProfileUpdateForm

# Create your views here.


def profile(request, user_id):
    try:
        profile_owner = Profile.objects.get(user=user_id)
    except Profile.DoesNotExist:
        return redirect("tweet_list")

    return render(request, "profile/profile.html", {"profile_owner": profile_owner})


@login_required
def edit_profile(request, user_id):
    try:
        profile_owner = Profile.objects.get(user=user_id)

        if request.method == "POST":
            form = UserProfileUpdateForm(
                request.POST, request.FILES, instance=profile_owner
            )
            if form.is_valid():
                profile = form.save(commit=False)
                profile.save()
                return redirect(reverse("profile", kwargs={"user_id": user_id}))
        else:
            form = UserProfileUpdateForm(instance=profile_owner)
            return render(
                request,
                "profile/edit_profile.html",
                {"form": form, "profile_owner": profile_owner},
            )

    except Profile.DoesNotExist:
        return redirect("tweet_list")
