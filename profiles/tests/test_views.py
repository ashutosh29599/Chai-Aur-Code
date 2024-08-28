from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from profiles.models import Profile


class ProfileTest(TestCase):
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


class ProfileViewTest(ProfileTest):
    def test_profile_GET_valid_data(self):
        response = self.client.get(reverse('profile', kwargs={'user_id': self.user.id}))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile/profile.html')

    def test_profile_GET_invalid_data_profile_does_not_exist(self):
        response = self.client.get(reverse('profile', kwargs={'user_id': 10}))

        self.assertEqual(response.status_code, 404)

    def test_profile_ajax(self):
        response = self.client.get(reverse('profile', kwargs={'user_id': self.user.id}), HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'partials/tweet_list.html')


class ProfileEditTest(ProfileTest):
    def setUp(self):
        super().setUp()

        self.profile.first_name = 'Test'
        self.profile.last_name = 'User'
        self.profile.email = self.user.email
        self.profile.bio = 'This is the test user\'s profile!'
        self.profile.save()

    def test_edit_profile_GET(self):
        response = self.client.get(reverse('edit_profile', kwargs={'user_id': self.user.id}))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile/edit_profile.html')

    def test_edit_profile_GET_profile_does_not_exist(self):
        response = self.client.get(reverse('edit_profile', kwargs={'user_id': 10}))

        self.assertEqual(response.status_code, 404)

    def test_edit_profile_POST_valid_data(self):
        updated_data = {
            'first_name': 'Testing',
            'last_name': 'User',
            'email': self.user.email, 
            'bio': 'This is the updated bio!'
        }

        response = self.client.post(reverse('edit_profile', kwargs={'user_id': self.user.id}), data=updated_data)
        self.profile.refresh_from_db()

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('profile', kwargs={'user_id': self.user.id}))

        self.assertEqual(self.profile.first_name, updated_data['first_name'])
        self.assertEqual(self.profile.last_name, updated_data['last_name'])
        self.assertEqual(self.profile.email, updated_data['email'])
        self.assertEqual(self.profile.bio, updated_data['bio'])

    def test_edit_profile_POST_invalid_data(self):
        updated_data = {}

        response = self.client.post(reverse('edit_profile', kwargs={'user_id': self.user.id}), data=updated_data)
        self.profile.refresh_from_db()

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('tweet_home'))
