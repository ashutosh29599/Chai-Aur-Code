from django.urls import reverse

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from django.contrib.auth.models import User

from profiles.models import Profile

from .utils import scroll_and_click


class UserProfileFactory:
    @staticmethod
    def create_user(username='test_user', password='super_secret_pwd_1234'):
        User.objects.create_user(username=username, password=password)

    @staticmethod
    def create_profile_for_test_user(username='test_user'):
        user = User.objects.get(username=username)
        Profile.objects.create(user=user, email=user.email)
    
    @staticmethod
    def login_user(browser, live_server_url, username, password):
        url = live_server_url + reverse('login')
        browser.get(url)

        browser.find_element(By.NAME, 'username').send_keys(username)
        browser.find_element(By.NAME, 'password').send_keys(password)

        login_btn = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@name='login']"))
        )

        scroll_and_click(browser=browser, element=login_btn)

    @staticmethod    
    def logout_user(browser):
        logout_btn = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@name='logout']"))
        )

        scroll_and_click(browser=browser, element=logout_btn)
    
    @staticmethod
    def go_to_user_profile(browser):
        profile_btn = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//a[@name="profile_btn"]'))
        )

        scroll_and_click(browser=browser, element=profile_btn)


class PostsFactory:
    @staticmethod
    def create_a_post(browser, post_text):
        create_post_btn = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[@name='create_post_btn']"))
        )
        scroll_and_click(browser=browser, element=create_post_btn)

        post_btn = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@name='post_post_btn']"))
        )

        browser.find_element(By.NAME, 'text').send_keys(post_text)
        
        scroll_and_click(browser=browser, element=post_btn)

    @staticmethod    
    def go_to_edit_post(browser):
        edit_btn = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//i[@class='bi bi-pencil']"))
        )
        
        scroll_and_click(browser=browser, element=edit_btn)

    @staticmethod
    def click_on_delete_post(browser):
        delete_btn = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//i[@class='bi bi-trash']"))
        )
        
        scroll_and_click(browser=browser, element=delete_btn)
