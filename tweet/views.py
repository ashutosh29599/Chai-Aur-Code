from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from django.urls import reverse
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User


from .models import Tweet
from profiles.models import Profile
from .forms import TweetForm

# Create your views here.


def index(request):
    return render(request, "index.html")


def tweet_list(request):
    if request.method == "POST":
        sorting_criteria = request.POST.get("sort_by")
        if sorting_criteria == "latest_first":
            tweets = Tweet.objects.all().order_by("-created_at")
        elif sorting_criteria == "oldest_first":
            tweets = Tweet.objects.all().order_by("created_at")
        elif sorting_criteria == "username_asc":
            tweets = Tweet.objects.all().order_by("user__username")
        elif sorting_criteria == "username_desc":
            tweets = Tweet.objects.all().order_by("-user__username")
    else:
        tweets = Tweet.objects.all().order_by("-created_at")
        sorting_criteria = "default"

    return render(request, "tweet_list.html", {"tweets": tweets, "sorting_criteria": sorting_criteria})


def tweet_search(request):
    if request.method == "POST":
        query = request.POST.get("search")

        if query:
            tweets = Tweet.objects.filter(text__icontains=query).order_by("-created_at")
            # users_queried = User.objects.filter(username__icontains=query).order_by("username")
            # profiles_queried = Profile.objects.filter(user__username__icontains=query).order_by("user__username")
            # users_and_profiles_queried = zip(users_queried, profiles_queried)

            profiles_queried = Profile.objects.filter(
                Q(user__username__icontains=query) | Q(first_name__icontains=query) | Q(last_name__icontains=query)
            ).order_by('user__username')

            users_queried = User.objects.filter(id__in=profiles_queried.values('user')).order_by('username')
            
            users_and_profiles_queried = zip(users_queried, profiles_queried)

            return render(
                request,
                "tweet_list.html",
                {"tweets": tweets, "search": True, "query": query, "users_and_profiles_queried": users_and_profiles_queried},
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
