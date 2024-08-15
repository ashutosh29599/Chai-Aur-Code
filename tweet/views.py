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


def get_tweet_sorting_map():
    sorting_map = {
        "default": "-created_at",
        "latest_first": "-created_at",
        "oldest_first": "created_at",
        "username_asc": "user__username",
        "username_desc": "-user__username",
    }

    return sorting_map


def get_user_sorting_maps():
    profile_sorting_map = {
        "default": "user__username",
        "username_asc": "user__username",
        "username_desc": "-user__username",
        "oldest_ac_first": "user__date_joined",
        "youngest_ac_first": "-user__date_joined",
    }

    user_sorting_map = {
        "default": "username",
        "username_asc": "username",
        "username_desc": "-username",
        "oldest_ac_first": "date_joined",
        "youngest_ac_first": "-date_joined",
    }

    return profile_sorting_map, user_sorting_map


def tweet_home(request):
    sorting_map = get_tweet_sorting_map()
    sorting_criteria = request.POST.get("sort_by", "default")
    tweets = Tweet.objects.all().order_by(sorting_map[sorting_criteria])

    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        # Render the partial template if this is an AJAX request
        return render(request, "partials/tweet_list.html", {"tweets": tweets})

    return render(
        request,
        "tweet_home.html",
        {"tweets": tweets, "sorting_criteria": sorting_criteria},
    )


def tweet_search(request):
    if (request.method == "POST" or request.headers.get("x-requested-with") == "XMLHttpRequest"):
        query = request.POST.get("search")
        tweet_sorting_criteria = request.POST.get("sort_by", "default")
        user_sorting_criteria = request.POST.get("sort_by_user", "default")
        sort_element = request.POST.get("sort_element", "users")

        profile_sorting_map, user_sorting_map = get_user_sorting_maps()

        if query:
            tweet_sorting_map = get_tweet_sorting_map()
            tweets = Tweet.objects.filter(text__icontains=query).order_by(tweet_sorting_map[tweet_sorting_criteria])

            profiles_queried = Profile.objects.filter(
                Q(user__username__icontains=query)
                | Q(first_name__icontains=query)
                | Q(last_name__icontains=query)
            ).order_by(profile_sorting_map[user_sorting_criteria])

            users_queried = User.objects.filter(id__in=profiles_queried.values("user")).order_by(user_sorting_map[user_sorting_criteria])

            users_and_profiles_queried = zip(users_queried, profiles_queried)

            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                if sort_element == "users":
                    template_to_render = "partials/user_list.html"
                else:
                    template_to_render = "partials/tweet_list.html"

                return render(request, 
                              template_to_render, 
                              {
                                  "tweets": tweets, 
                                  "users_and_profiles_queried": users_and_profiles_queried,
                                  "users_count": len(users_queried)
                            },
                        )

            return render(
                request,
                "tweet_search.html",
                {
                    "tweets": tweets,
                    "search": True,
                    "query": query,
                    "users_and_profiles_queried": users_and_profiles_queried,
                    "users_count": len(users_queried),
                },
            )

    return redirect("tweet_home")

def users(request):
    user_sorting_criteria = request.POST.get("sort_by_user", "default")
    profile_sorting_map, user_sorting_map = get_user_sorting_maps()

    profiles_queried = Profile.objects.all().order_by(profile_sorting_map[user_sorting_criteria])
    users_queried = User.objects.all().order_by(user_sorting_map[user_sorting_criteria])

    users_and_profiles_queried = zip(users_queried, profiles_queried)

    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        template_to_render = "partials/user_list.html"
    else:
        template_to_render = "users.html"

    return render(request, 
                  template_to_render, 
                  {
                    "users_and_profiles_queried": users_and_profiles_queried,
                    "users_count": len(users_queried),
                    "page": "users",
                  }
                )

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
