from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class TweetManager(models.Manager):
    def get_tweets_for_user(self, user):
        return self.filter(user=user).order_by("-created_at")


class Tweet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(max_length=240)
    photo = models.ImageField(upload_to="photos/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = TweetManager()

    def __str__(self) -> str:
        return f"{self.user.username} - {self.text[:10]}"
