"""
    X 1) Check with no users, verify the page doesn't have any users
    X 2) Create one user, verify they exist on this page.
    3) Create multiple users
        3.1) Verify the sort functionality.
"""

from django.contrib.auth.models import User
from django.urls import reverse

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

from .base import IntegrationTest
from .factories import UserProfileFactory, PostsFactory

import time


class UserPageTest(IntegrationTest):
    def test_go_to_user_page_with_no_users_registered(self):
        self.browser.get(self.live_server_url + reverse('tweet_home'))

        user_page_btn = WebDriverWait(self.browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[@name='user_page_btn']"))
        )

        user_page_btn.click()

        WebDriverWait(self.browser, 10).until(
            EC.url_matches(self.live_server_url + reverse('users'))
        )

        self.assertEqual(self.browser.title, 'Users')
        with self.assertRaises(NoSuchElementException):
            self.browser.find_element(By.CLASS_NAME, 'card')
            # self.browser.find_element(By.XPATH, "//div[@class='card']")
    
    def test_go_to_user_page_with_one_user(self):
        UserProfileFactory.create_user(
            username='test_user', password='super_secret_pwd_1234', email='test_user@domain.com'
        )
        UserProfileFactory.create_profile_for_test_user(username='test_user')
        UserProfileFactory.set_test_user_name(username='test_user', first_name='Test', last_name='User')

        self.browser.get(self.live_server_url + reverse('users'))

        WebDriverWait(self.browser, 10).until(
            EC.url_matches(self.live_server_url + reverse('users'))
        )

        name = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//h5[@class='card-title']"))
        ).text

        self.assertEqual(name, 'Test User')

    def test_go_to_user_profile_from_user_page(self):
        UserProfileFactory.create_user(
            username='test_user', password='super_secret_pwd_1234', email='test_user@domain.com'
        )
        UserProfileFactory.create_profile_for_test_user(username='test_user')
        UserProfileFactory.set_test_user_name(username='test_user', first_name='Test', last_name='User')

        self.browser.get(self.live_server_url + reverse('users'))

        user_profile_btn = WebDriverWait(self.browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[@name='user_profile_btn']"))
        )
        user_profile_btn.click()

        WebDriverWait(self.browser, 10).until(
            EC.url_matches(self.live_server_url + reverse('profile', kwargs={'user_id': User.objects.get(username='test_user').id}))
        )

        self.assertEqual(self.browser.title, 'Profile')
        self.assertIn('test_user', self.browser.page_source)

    def test_users_sorted_by_username_ascending(self):
        users = PostsFactory.create_users_and_get_them_back_after_sorting_from_users_page(
            browser=self.browser, live_server_url=self.live_server_url, sort_by='username_asc'
        )

        self.assertEqual(users, ['A. Test User', 'B. Test User'])

    def test_users_sorted_by_username_descending(self):
        users = PostsFactory.create_users_and_get_them_back_after_sorting_from_users_page(
            browser=self.browser, live_server_url=self.live_server_url, sort_by='username_desc'
        )

        self.assertEqual(users, ['B. Test User', 'A. Test User'])

    def test_users_sorted_by_old_accounts_first(self):
        users = PostsFactory.create_users_and_get_them_back_after_sorting_from_users_page(
            browser=self.browser, live_server_url=self.live_server_url, sort_by='oldest_ac_first'
        )

        self.assertEqual(users, ['A. Test User', 'B. Test User'])

    def test_users_sorted_by_newest_accounts_first(self):
        users = PostsFactory.create_users_and_get_them_back_after_sorting_from_users_page(
            browser=self.browser, live_server_url=self.live_server_url, sort_by='youngest_ac_first'
        )

        self.assertEqual(users, ['B. Test User', 'A. Test User'])
