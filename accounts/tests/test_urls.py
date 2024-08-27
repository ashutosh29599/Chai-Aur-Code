from django.test import SimpleTestCase
from django.urls import reverse, resolve
from django.contrib.auth import views as auth_views

from accounts.views import register, change_password

class URLTests(SimpleTestCase):
    def test_register_url_resolves(self):
        url = reverse('register')
        self.assertEqual(resolve(url).func, register)

    def test_change_password_url_resolves(self):
        self.assertEqual(resolve(reverse('change_password')).func, change_password)

    def test_password_reset_url_resolves(self):
        url = reverse('password_reset')
        self.assertEqual(resolve(url).func.view_class, auth_views.PasswordResetView)
    
    def test_password_reset_done_url_resolves(self):
        url = reverse('password_reset_done')
        self.assertEqual(resolve(url).func.view_class, auth_views.PasswordResetDoneView)

    def test_password_reset_confirm_url_resolves(self):
        url = reverse('password_reset_confirm', kwargs={'uidb64': 'uid', 'token': 'token'})
        self.assertEqual(resolve(url).func.view_class, auth_views.PasswordResetConfirmView)

    def test_password_reset_complete_url_resolves(self):
        url = reverse('password_reset_complete')
        self.assertEqual(resolve(url).func.view_class, auth_views.PasswordResetCompleteView)    