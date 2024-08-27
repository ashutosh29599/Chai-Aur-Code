from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from profiles.models import Profile


class UserRegistrationViewTest(TestCase):
    def test_canary(self):
        self.assertTrue(True)

    def test_register_view_GET(self):
        response = self.client.get(reverse("register"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/register.html")

    def test_register_view_POST_valid_data(self):
        data = {
            "username": "test_user",
            "email": "test_user@domain.com",
            "password1": "super_secret_pwd_1",
            "password2": "super_secret_pwd_1",
        }

        response = self.client.post(reverse("register"), data=data)

        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(Profile.objects.count(), 1)

        self.assertRedirects(response, reverse("tweet_home"))

    def test_register_view_POST_invalid_data(self):
        data = {
            "username": "test_user",
            "email": "test_user@domain.com",
            "password1": "super_secret_pwd_1",
            "password2": "different_pwd",
        }

        response = self.client.post(reverse("register"), data=data)

        self.assertEqual(User.objects.count(), 0)
        self.assertEqual(Profile.objects.count(), 0)

        self.assertContains(response, "The two password fields didn’t match.")

        self.assertTemplateUsed("registration/register.html")


class ChangePasswordViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="test_user", password="old_password_123"
        )
        Profile.objects.create(user=self.user, email=self.user.email)

        self.client.login(username="test_user", password="old_password_123")

    def test_change_pwd_GET(self):
        response = self.client.get(reverse("change_password"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "change_password/change_password.html")

    def test_change_pwd_POST_valid_data(self):
        data = {
            "old_password": "old_password_123",
            "new_password1": "new_password_123",
            "new_password2": "new_password_123",
        }

        response = self.client.post(reverse("change_password"), data=data)

        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("new_password_123"))

        self.assertRedirects(
            response, reverse("profile", kwargs={"user_id": self.user.id})
        )

    def test_change_pwd_POST_invalid_data_new_pwd_do_not_match(self):
        data = {
            "old_password": "old_password_123",
            "new_password1": "new_password_123",
            "new_password2": "different_new_password_123",
        }

        response = self.client.post(reverse("change_password"), data=data)

        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("old_password_123"))

        self.assertContains(response, "The two password fields didn’t match.")

        self.assertTemplateUsed(response, "change_password/change_password.html")

    def test_change_pwd_POST_invalid_old_password(self):
        data = {
            "old_password": "some_different_old_password_123",
            "new_password1": "new_password_123",
            "new_password2": "new_password_123",
        }

        response = self.client.post(reverse("change_password"), data=data)

        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("old_password_123"))

        self.assertContains(
            response,
            "Your old password was entered incorrectly. Please enter it again.",
        )

        self.assertTemplateUsed(response, "change_password/change_password.html")
