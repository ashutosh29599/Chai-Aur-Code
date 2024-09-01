"""
    1) Create a post
    2) Edit post
    3) Delete post
    4) Click on username on post, verify if it redirects to profile
    5) Sorting
        5.1) Latest first
        5.2) Oldest first
        5.3) Username asc
        5.4) Username des
"""

from django.contrib.auth.models import User

from django.urls import reverse

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.service import Service
# from selenium.webdriver.firefox.options import Options 
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

from .base import IntegrationTest
from .factories import UserProfileFactory, PostsFactory

from .utils import scroll_and_click

import time


class PostsTest(IntegrationTest):
    def test_create_a_post(self):
        UserProfileFactory.create_user(
            username='test_user', password='super_secret_pwd_1234', email='test_user@domain.com'
        )
        UserProfileFactory.login_user(browser=self.browser, live_server_url=self.live_server_url,
                                      username='test_user', password='super_secret_pwd_1234')
        
        PostsFactory.create_a_post(browser=self.browser, post_text='This is the post text!')

        post_text = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//p[@name='post_text']"))
        ).text

        self.assertEqual(post_text, 'This is the post text!')

    def test_edit_post(self):
        UserProfileFactory.create_user(
            username='test_user', password='super_secret_pwd_1234', email='test_user@domain.com'
        )
        UserProfileFactory.login_user(browser=self.browser, live_server_url=self.live_server_url,
                                      username='test_user', password='super_secret_pwd_1234')
        
        PostsFactory.create_a_post(browser=self.browser, post_text='This is the post text!')

        edit_btn = WebDriverWait(self.browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//i[@class='bi bi-pencil']"))
        )
        scroll_and_click(browser=self.browser, element=edit_btn)

        post_btn = WebDriverWait(self.browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@name='post_post_btn']"))
        )

        post_text_element = self.browser.find_element(By.NAME, 'text')
        post_text_element.clear()
        post_text_element.send_keys('This is the updated post test!')
        
        scroll_and_click(browser=self.browser, element=post_btn)

        post_text = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//p[@name='post_text']"))
        ).text

        self.assertEqual(post_text, 'This is the updated post test!')

    def test_edit_post_cancel(self):
        UserProfileFactory.create_user(
            username='test_user', password='super_secret_pwd_1234', email='test_user@domain.com'
        )
        UserProfileFactory.login_user(browser=self.browser, live_server_url=self.live_server_url,
                                      username='test_user', password='super_secret_pwd_1234')
        
        PostsFactory.create_a_post(browser=self.browser, post_text='This is the post text!')
        PostsFactory.go_to_edit_post(browser=self.browser)

        back_to_home_btn = WebDriverWait(self.browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[@name='back_to_home_btn']"))
        )
        scroll_and_click(browser=self.browser, element=back_to_home_btn)

        WebDriverWait(self.browser, 10).until(
            EC.url_matches(self.live_server_url + reverse('tweet_home'))
        )

        post_text = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//p[@name='post_text']"))
        ).text

        self.assertEqual(post_text, 'This is the post text!')

    def test_delete_post(self):
        UserProfileFactory.create_user(
            username='test_user', password='super_secret_pwd_1234', email='test_user@domain.com'
        )
        UserProfileFactory.login_user(browser=self.browser, live_server_url=self.live_server_url,
                                      username='test_user', password='super_secret_pwd_1234')
        
        PostsFactory.create_a_post(browser=self.browser, post_text='This is the post text!')
        PostsFactory.click_on_delete_post(browser=self.browser)
        
        delete_btn = WebDriverWait(self.browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@name='delete_btn']"))
        )
        scroll_and_click(browser=self.browser, element=delete_btn)

        self.assertNotIn('This is the post text!', self.browser.page_source)
    
    def test_delete_post_cancel(self):
        UserProfileFactory.create_user(
            username='test_user', password='super_secret_pwd_1234', email='test_user@domain.com'
        )
        UserProfileFactory.login_user(browser=self.browser, live_server_url=self.live_server_url,
                                      username='test_user', password='super_secret_pwd_1234')
        
        PostsFactory.create_a_post(browser=self.browser, post_text='This is the post text!')
        PostsFactory.click_on_delete_post(browser=self.browser)

        cancel_btn = WebDriverWait(self.browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[@name='cancel_btn']"))
        )
        scroll_and_click(browser=self.browser, element=cancel_btn)

        post_text = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//p[@name='post_text']"))
        ).text

        self.assertEqual(post_text, 'This is the post text!')

    def test_go_to_post_user(self):
        UserProfileFactory.create_user(
            username='test_user', password='super_secret_pwd_1234', email='test_user@domain.com'
        )
        UserProfileFactory.login_user(browser=self.browser, live_server_url=self.live_server_url,
                                      username='test_user', password='super_secret_pwd_1234')
        UserProfileFactory.create_profile_for_test_user(username='test_user')
        
        PostsFactory.create_a_post(browser=self.browser, post_text='This is the post text!')

        user_profile_btn = WebDriverWait(self.browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[@name='username']"))
        )
        scroll_and_click(browser=self.browser, element=user_profile_btn)

        WebDriverWait(self.browser, 10).until(
            EC.url_matches(self.live_server_url + reverse('profile', kwargs={'user_id': User.objects.get(username=user_profile_btn.text).id}))
        )

        self.assertEqual(self.browser.title, 'Profile')


class PostsSortingTest(IntegrationTest):
    def test_sorting_latest_first(self): 
        posts = PostsFactory.create_posts_from_multiple_users_for_sorting(
            browser=self.browser,
            live_server_url=self.live_server_url,
            sort_by='latest_first'
        )

        self.assertEqual(posts, ['This post is by b_test_user!', 'This post is by a_test_user!'])

    def test_sorting_oldest_first(self):
        posts = PostsFactory.create_posts_from_multiple_users_for_sorting(
            browser=self.browser,
            live_server_url=self.live_server_url,
            sort_by='oldest_first'
        )

        self.assertEqual(posts, ['This post is by a_test_user!', 'This post is by b_test_user!'])

    def test_sorting_username_ascending(self):
        posts = PostsFactory.create_posts_from_multiple_users_for_sorting(
            browser=self.browser,
            live_server_url=self.live_server_url,
            sort_by='username_asc'
        )
        
        self.assertEqual(posts, ['This post is by a_test_user!', 'This post is by b_test_user!'])

    def test_sorting_username_descending(self):
        posts = PostsFactory.create_posts_from_multiple_users_for_sorting(
            browser=self.browser,
            live_server_url=self.live_server_url,
            sort_by='username_desc'
        )
        
        self.assertEqual(posts, ['This post is by b_test_user!', 'This post is by a_test_user!'])
