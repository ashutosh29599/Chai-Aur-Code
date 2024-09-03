"""
    1) Posts
        1.1) Search for existing posts
        1.2) Search for non-existing posts
        1.3) Verify the sort functionality
    2) Users
        2.1) Search for exists users
        2.2) Search for non-existing users
        2.3) Verify the sort functionality
"""

from django.contrib.auth.models import User
from django.urls import reverse

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC

from .base import IntegrationTest
from .factories import UserProfileFactory, PostsFactory

from .utils import scroll_and_click

import time


class SearchTest(IntegrationTest):
    def setUp(self):
        super().setUp()

        UserProfileFactory.create_user(
            username='test_user', password='super_secret_pwd_1234', email='test_user@domain.com'
        )
        UserProfileFactory.create_profile_for_test_user(username='test_user')
        UserProfileFactory.set_test_user_name(username='test_user', first_name='Test', last_name='User')

    def search(self, query):
        self.browser.get(self.live_server_url + reverse('tweet_home'))

        search_btn = WebDriverWait(self.browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@name='search_btn']"))
        )
        self.browser.find_element(By.NAME, 'search').send_keys(query)
        search_btn.click()

    def test_search_test_user(self):
        self.search('test_user')

        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.ID, "users-queried"))
        )

        users_btn = WebDriverWait(self.browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@id='btncheck-users']"))
        )
        scroll_and_click(browser=self.browser, element=users_btn)

        self.assertIn('Users containing "test_user"', self.browser.page_source)
        self.assertIn('<h5 class="card-title">Test User</h5>', self.browser.page_source)

    def test_search_post(self):
        UserProfileFactory.login_user(
            browser=self.browser,
            live_server_url=self.live_server_url,
            username='test_user',
            password='super_secret_pwd_1234'
        )
        PostsFactory.create_a_post(browser=self.browser, post_text='This is a post!')

        self.search('post')

        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.ID, "tweets-queried"))
        )

        self.assertIn('Tweets containing "post"', self.browser.page_source)
        self.assertIn('<p class="card-text" name="post_text">This is a post!</p>', self.browser.page_source)
