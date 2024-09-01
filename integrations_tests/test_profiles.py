from django.contrib.auth.models import User

from django.test import LiveServerTestCase
from django.urls import reverse

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.service import Service
# from selenium.webdriver.firefox.options import Options 
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from .base import IntegrationTest
from .factories import UserProfileFactory

from .utils import scroll_and_click


class UserProfileTest(IntegrationTest):
    def test_go_to_user_profile(self):
        UserProfileFactory.create_user(
            username='test_user', password='super_secret_pwd_1234', email='test_user@domain.com'
        )
        UserProfileFactory.login_user(browser=self.browser, live_server_url=self.live_server_url,
                                      username='test_user', password='super_secret_pwd_1234')
        UserProfileFactory.create_profile_for_test_user(username='test_user')
        UserProfileFactory.go_to_user_profile(browser=self.browser)

        WebDriverWait(self.browser, 10).until(
            EC.url_matches(self.live_server_url + reverse('profile', kwargs={'user_id': User.objects.all()[0].id}))
        )
        
        self.assertEqual(self.browser.title, 'Profile')

    def test_edit_profile(self):
        UserProfileFactory.create_user(
            username='test_user', password='super_secret_pwd_1234', email='test_user@domain.com'
        )
        UserProfileFactory.login_user(browser=self.browser, live_server_url=self.live_server_url,
                                      username='test_user', password='super_secret_pwd_1234')
        UserProfileFactory.create_profile_for_test_user(username='test_user')
        UserProfileFactory.go_to_user_profile(browser=self.browser)

        edit_profile_btn = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//a[@name='edit_profile_btn']"))
        )
        scroll_and_click(browser=self.browser, element=edit_profile_btn)

        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.XPATH, '//h1[contains(text(), "Update your profile,")]'))
        )
        self.browser.find_element(By.NAME, 'first_name').send_keys('Test')
        self.browser.find_element(By.NAME, 'last_name').send_keys('User')
        self.browser.find_element(By.NAME, 'bio').send_keys('This is the test user\'s bio!')

        email = self.browser.find_element(By.NAME, 'email')
        email.clear()
        email.send_keys('test_user@domain.com')

        update_btn = WebDriverWait(self.browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@name='update_btn']"))
        )
        scroll_and_click(browser=self.browser, element=update_btn)

        WebDriverWait(self.browser, 10).until(
            EC.url_changes(self.browser.current_url)
        )

        # verify that the profile details can be seen
        name = self.browser.find_element(By.XPATH, "//input[@name='name']").get_attribute('value').strip()
        email = self.browser.find_element(By.XPATH, "//input[@name='email']").get_attribute('value').strip()
        bio = self.browser.find_element(By.XPATH, "//textarea[@name='bio']").get_attribute('value').strip()

        self.assertEqual(name, 'Test User')
        self.assertEqual(email, 'test_user@domain.com')
        self.assertEqual(bio, 'This is the test user\'s bio!')
