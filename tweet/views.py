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


def tweet_fetch_by_sorting(sorting_criteria):
    sorting_map = {
        "latest_first": "-created_at",
        "oldest_first": "created_at",
        "username_asc": "user__username",
        "username_desc": "-user__username"
    }

    tweets = Tweet.objects.all().order_by(sorting_map.get(sorting_criteria, "-created_at"))

    return tweets
    

def tweet_home(request):
    if request.method == "POST":
        sorting_criteria = request.POST.get("sort_by", "default")
    else:
        sorting_criteria = "default"

    tweets = tweet_fetch_by_sorting(sorting_criteria)

    return render(request, "tweet_home.html", {"tweets": tweets, "sorting_criteria": sorting_criteria})


def tweet_search(request):
    if request.method == "POST":
        query = request.POST.get("search")

        if query:
            # tweets = Tweet.objects.filter(text__icontains=query).order_by("-created_at")
            tweets = tweet_fetch_by_sorting("default")
            
            profiles_queried = Profile.objects.filter(
                Q(user__username__icontains=query) | Q(first_name__icontains=query) | Q(last_name__icontains=query)
            ).order_by('user__username')

            users_queried = User.objects.filter(id__in=profiles_queried.values('user')).order_by('username')
            
            users_and_profiles_queried = zip(users_queried, profiles_queried)

            return render(
                request, 
                "tweet_search.html", 
                {
                    "tweets": tweets, 
                    "search": True, 
                    "query": query, 
                    "users_and_profiles_queried": users_and_profiles_queried,
                    "users_count": len(users_queried)
                    },
            )
    
    return redirect("tweet_home")


@login_required
def tweet_create(request):
    if request.method == "POST":
        form = TweetForm(request.POST, request.FILES)

        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.user = request.user
            tweet.save()

            return redirect("tweet_home")
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

            return redirect("tweet_home")
    else:
        form = TweetForm(instance=tweet)

    return render(request, "tweet_form.html", {"form": form})


@login_required
def tweet_delete(request, tweet_id):
    tweet = get_object_or_404(Tweet, pk=tweet_id, user=request.user)

    if request.method == "POST":
        tweet.delete()

        return redirect("tweet_home")

    return render(request, "tweet_confirm_delete.html", {"tweet": tweet})
