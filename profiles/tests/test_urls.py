from django.test import SimpleTestCase
from django.urls import reverse, resolve

from profiles.views import profile, edit_profile


class ProfileURLTest(SimpleTestCase):
    def test_profile_url_resolves(self):
        url = reverse('profile', kwargs={'user_id': 1})
        self.assertEqual(resolve(url).func, profile)

    def test_edit_profile_url_resolves(self):
        url = reverse('edit_profile', kwargs={'user_id': 1})
        self.assertEqual(resolve(url).func, edit_profile)
