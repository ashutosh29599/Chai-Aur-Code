from django.test import TestCase
from django.contrib.auth.models import User

from accounts.forms import UserRegistrationForm


class UserRegistrationFormTest(TestCase):
    def test_form_valid_data(self):
        data = {
            "username": "test_user",
            "email": "test_user@domain.com",
            "password1": "super_secret_pwd_1",
            "password2": "super_secret_pwd_1"
        }

        form = UserRegistrationForm(data)

        self.assertTrue(form.is_valid())

        form.save()

        user = User.objects.get(username=data['username'])
        self.assertTrue(user.username, data['username'])
        self.assertTrue(user.check_password(data['password1']))

    def test_form_invalid_data_short_password(self):
        data = {
            "username": "test_user",
            "email": "test_user@domain.com",
            "password1": "short",
            "password2": "short"
        }

        form = UserRegistrationForm(data)

        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)
        self.assertIn('password2', form.errors)
        self.assertIn('This password is too short. It must contain at least 8 characters.', form.errors['password2'])

    def test_form_invalid_email(self):
        data = {
            "username": "test_user",
            "email": "test_user",
            "password1": "super_secret_pwd_1",
            "password2": "super_secret_pwd_1"
        }

        form = UserRegistrationForm(data)

        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)
        self.assertIn('email', form.errors)
        self.assertIn('Enter a valid email address.', form.errors['email'])
    
    def test_form_required_fields(self):
        data = {}

        form = UserRegistrationForm(data)

        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)
        self.assertIn('email', form.errors)
        self.assertIn('password1', form.errors)
        self.assertIn('password2', form.errors)
