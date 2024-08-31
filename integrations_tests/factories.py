from django.urls import reverse

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from django.contrib.auth.models import User


from profiles.models import Profile


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

        browser.execute_script("arguments[0].scrollIntoView(true);", login_btn)
        browser.execute_script("arguments[0].click();", login_btn)

    @staticmethod    
    def logout_user(browser):
        logout_btn = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@name='logout']"))
        )

        browser.execute_script("arguments[0].scrollIntoView(true);", logout_btn)
        browser.execute_script("arguments[0].click();", logout_btn)
    
    @staticmethod
    def go_to_user_profile(browser):
        profile_btn = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//a[@name="profile_btn"]'))
        )
        
        browser.execute_script("arguments[0].click();", profile_btn)

