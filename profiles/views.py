from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from django.urls import reverse

from .models import Profile
from .forms import UserProfileUpdateForm

from tweet.models import Tweet
from tweet.views import get_post_sorting_map

# Create your views here.


def profile(request, user_id):    # try:
    profile_owner = get_object_or_404(Profile, user=user_id)

    post_sorting_criteria = request.POST.get("sort_by", "default")
    post_sorting_map = get_post_sorting_map()

    tweets = Tweet.objects.get_tweets_for_user(user_id, post_sorting_map[post_sorting_criteria])

    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return render(request, "partials/tweet_list.html", {"tweets": tweets})
    
    return render(request, "profile/profile.html", {"profile_owner": profile_owner, "tweets": tweets, "page": "profile"})


@login_required
def edit_profile(request, user_id):
    profile_owner = get_object_or_404(Profile, user=user_id)

    if request.method == "POST":
        form = UserProfileUpdateForm(
            request.POST, request.FILES, instance=profile_owner
        )
        if form.is_valid():
            profile = form.save(commit=False)
            profile.save()
            return redirect(reverse("profile", kwargs={"user_id": user_id}))
        return redirect(reverse("tweet_home"))

    else:
        form = UserProfileUpdateForm(instance=profile_owner)
        return render(
            request,
            "profile/edit_profile.html",
            {"form": form, "profile_owner": profile_owner},
        )
