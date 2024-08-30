from django.contrib.auth.models import User

from django.test import LiveServerTestCase
from django.urls import reverse

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

from profiles.models import Profile

import time


class UserRegistrationFunctionalTest(LiveServerTestCase):
    def setUp(self):
        gecko_driver_path = '/Users/ashutosh/Desktop/Programming/Django/Chai-Aur-Tweet/geckodriver'
        service = Service(executable_path=gecko_driver_path)
        # options = Options()

        self.browser = webdriver.Firefox(service=service)
    
    def tearDown(self):
        self.browser.quit()
        User.objects.all().delete()
        # pass

    def create_user_and_login(self):
        User.objects.create_user(username='test_user', password='super_secret_pwd_1234')

        url = self.live_server_url + reverse('login')
        self.browser.get(url)

        self.browser.find_element(By.NAME, 'username').send_keys('test_user')
        self.browser.find_element(By.NAME, 'password').send_keys('super_secret_pwd_1234')

        login_btn = WebDriverWait(self.browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@name='login']"))
        )

        self.browser.execute_script("arguments[0].scrollIntoView(true);", login_btn)
        self.browser.execute_script("arguments[0].click();", login_btn)

    def create_profile_for_test_user(self):
        Profile.objects.create(user=User.objects.get(username='test_user'))

    def go_to_user_profile(self):
        profile_btn = WebDriverWait(self.browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//a[@name="profile_btn"]'))
        )
        
        self.browser.execute_script("arguments[0].click();", profile_btn)

    def test_register_a_new_account(self):
        url = self.live_server_url + reverse('register')
        self.browser.get(url)

        self.browser.find_element(By.NAME, 'username').send_keys('test_user')
        self.browser.find_element(By.NAME, 'email').send_keys('test_user@domain.com')
        self.browser.find_element(By.NAME, 'password1').send_keys('super_secret_pwd_1234')
        self.browser.find_element(By.NAME, 'password2').send_keys('super_secret_pwd_1234')

        # Wait for the register button to be clickable and click it
        register_button = WebDriverWait(self.browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@name='register']"))
        )
        
        # Scroll into view if necessary
        self.browser.execute_script("arguments[0].scrollIntoView(true);", register_button)
        
        # Click the button
        self.browser.execute_script("arguments[0].click();", register_button)

        WebDriverWait(self.browser, 10).until(EC.url_changes(self.browser.current_url))

        expected_url = self.live_server_url + reverse('tweet_home')
        self.assertEqual(self.browser.current_url, expected_url)

    def test_login_with_new_account(self):
        self.create_user_and_login()

        WebDriverWait(self.browser, 10).until(EC.url_changes(self.browser.current_url))

        expected_url = self.live_server_url + reverse('tweet_home')
        self.assertEqual(self.browser.current_url, expected_url)

    def test_logout(self):
        self.create_user_and_login()

        logout_btn = WebDriverWait(self.browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@name='logout']"))
        )

        self.browser.execute_script("arguments[0].scrollIntoView(true);", logout_btn)
        self.browser.execute_script("arguments[0].click();", logout_btn)

        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//button[@name='logout']"))
        )

        self.assertTrue(EC.element_to_be_clickable((By.XPATH, "//button[@name='login']")))

    def test_go_to_user_profile(self):
        self.create_user_and_login()
        self.create_profile_for_test_user()

        # go to profile
        self.go_to_user_profile()

        welcome_msg = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.XPATH, '//h1[@name="profile_welcome_msg"]'))
        ).text
        self.assertIn("Welcome to your profile, test_user!", welcome_msg)

    # def test_edit_profile(self):
    #     pass

    # def test_change_password(self):
        # click on change pwd
        # change the pwd
        # logout
        # try logging in again with new pwd
    #     pass


