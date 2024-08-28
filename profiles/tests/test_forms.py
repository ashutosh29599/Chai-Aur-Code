from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from profiles.models import Profile
from profiles.forms import UserProfileUpdateForm


class UserProfileUpdateFormTest(TestCase):
    def setUp(self):
        data = {
            "username": "test_user",
            "email": "test_user@domain.com",
            "password1": "super_secret_pwd_1",
            "password2": "super_secret_pwd_1",
        }

        self.client.post(reverse("register"), data=data)

        self.user = User.objects.get(username=data['username'])
        self.profile = Profile.objects.get(user=self.user)

        self.client.login(username=data['username'], password=data['password1'])

    def test_user_profile_form_valid_data(self):
        data = {
            'first_name': 'Test',
            'last_name': 'User',
            'email': self.user.email, 
            'bio': 'This is the bio!'
        }

        form = UserProfileUpdateForm(data, instance=self.profile)

        self.assertTrue(form.is_valid())
        form.save()

        self.profile.refresh_from_db()

        self.assertEqual(self.profile.first_name, data['first_name'])
        self.assertEqual(self.profile.last_name, data['last_name'])
        self.assertEqual(self.profile.email, data['email'])
        self.assertEqual(self.profile.bio, data['bio'])

    def test_user_profile_form_invalid_data_email_missing(self):
        data = {
            'first_name': 'Test',
            'last_name': 'User',
            'bio': 'This is the bio!'
        }

        form = UserProfileUpdateForm(data, instance=self.profile)

        self.assertFalse(form.is_valid())
        