from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User


from .models import Tweet, Profile
from .forms import TweetForm, UserRegistrationForm, UserProfileUpdateForm

# Create your views here.


def index(request):
    return render(request, "index.html")


def tweet_list(request):
    tweets = Tweet.objects.all().order_by("-created_at")

    return render(request, "tweet_list.html", {"tweets": tweets})


def tweet_search(request):
    if request.method == "POST":
        query = request.POST.get("search")

        if query:
            tweets = Tweet.objects.filter(text__icontains=query).order_by("-created_at")
            return render(
                request,
                "tweet_list.html",
                {"tweets": tweets, "search": True, "query": query},
            )

    return redirect("tweet_list")


@login_required
def tweet_create(request):
    if request.method == "POST":
        form = TweetForm(request.POST, request.FILES)

        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.user = request.user
            tweet.save()

            return redirect("tweet_list")
    else:
        form = TweetForm()

    return render(request, "tweet_form.html", {"form": form})


@login_required
def tweet_edit(request, tweet_id):
    tweet = get_object_or_404(Tweet, pk=tweet_id, user=request.user)

    if request.method == "POST":
        form = TweetForm(request.POST, request.FILES, instance=tweet)

        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.user = request.user
            tweet.save()

            return redirect("tweet_list")
    else:
        form = TweetForm(instance=tweet)

    return render(request, "tweet_form.html", {"form": form})


@login_required
def tweet_delete(request, tweet_id):
    tweet = get_object_or_404(Tweet, pk=tweet_id, user=request.user)

    if request.method == "POST":
        tweet.delete()

        return redirect("tweet_list")

    return render(request, "tweet_confirm_delete.html", {"tweet": tweet})


def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password1"])
            user.save()
            login(request, user)
            return redirect("tweet_list")
    else:
        form = UserRegistrationForm()

    return render(request, "registration/register.html", {"form": form})


def profile(request, user_id):
    # profile_owner = get_object_or_404(User, pk=user_id)
    # profile_owner = get_object_or_404(Profile, pk=user_id)
    
    try:
        profile_owner = Profile.objects.get(pk=user_id)
    except Profile.DoesNotExist:
        # return redirect("tweet_list")
        profile_owner = Profile()

    return render(request, "profile/profile.html", {"profile_owner": profile_owner})


@login_required
def edit_profile(request, user_id):
    try:
        profile_owner = Profile.objects.get(pk=user_id)
        form = UserProfileUpdateForm(
            first_name=profile_owner.first_name,
            last_name = profile_owner.last_name,
            email = profile_owner.email,
            bio = profile_owner.bio
            )
        return render(request, "profile/edit_profile.html", {"form": form, "profile_owner": profile_owner})
    except Profile.DoesNotExist:
        # return redirect("tweet_list")
        return render(request, "profile/edit_profile.html", {"form": UserProfileUpdateForm})

