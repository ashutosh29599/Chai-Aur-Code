from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    first_name = models.CharField(max_length=50, null=True)
    last_name = models.CharField(max_length=50, null=True)
    email = models.EmailField(unique=True)
    bio = models.TextField(max_length=240, blank=True, null=True)
    photo = models.ImageField(upload_to="profile_pictures/", blank=True, null=True)

    def __str__(self) -> str:
        return self.user.username
