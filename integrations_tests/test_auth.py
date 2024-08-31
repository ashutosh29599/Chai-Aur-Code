from django.contrib.auth.models import User

from django.test import LiveServerTestCase
from django.urls import reverse

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from .factories import UserProfileFactory

import time


class UserAuthTest(LiveServerTestCase):
    def setUp(self):
        gecko_driver_path = (
            "/Users/ashutosh/Desktop/Programming/Django/Chai-Aur-Tweet/geckodriver"
        )
        service = Service(executable_path=gecko_driver_path)
        # options = Options()

        self.browser = webdriver.Firefox(service=service)

    def tearDown(self):
        self.browser.quit()
        User.objects.all().delete()

    def test_register_a_new_account(self):
        url = self.live_server_url + reverse("register")
        self.browser.get(url)

        self.browser.find_element(By.NAME, "username").send_keys("test_user")
        self.browser.find_element(By.NAME, "email").send_keys("test_user@domain.com")
        self.browser.find_element(By.NAME, "password1").send_keys(
            "super_secret_pwd_1234"
        )
        self.browser.find_element(By.NAME, "password2").send_keys(
            "super_secret_pwd_1234"
        )

        # Wait for the register button to be clickable and click it
        register_button = WebDriverWait(self.browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@name='register']"))
        )

        # Scroll into view if necessary
        self.browser.execute_script(
            "arguments[0].scrollIntoView(true);", register_button
        )

        # Click the button
        self.browser.execute_script("arguments[0].click();", register_button)

        WebDriverWait(self.browser, 10).until(EC.url_changes(self.browser.current_url))

        expected_url = self.live_server_url + reverse("tweet_home")
        self.assertEqual(self.browser.current_url, expected_url)

    def test_login_with_new_account(self):
        UserProfileFactory.create_user(
            username="test_user", password="super_secret_pwd_1234"
        )
        UserProfileFactory.login_user(
            browser=self.browser,
            live_server_url=self.live_server_url,
            username="test_user",
            password="super_secret_pwd_1234",
        )

        WebDriverWait(self.browser, 10).until(EC.url_changes(self.browser.current_url))

        expected_url = self.live_server_url + reverse("tweet_home")
        self.assertEqual(self.browser.current_url, expected_url)

    def test_logout(self):
        UserProfileFactory.create_user(
            username="test_user", password="super_secret_pwd_1234"
        )
        UserProfileFactory.login_user(
            browser=self.browser,
            live_server_url=self.live_server_url,
            username="test_user",
            password="super_secret_pwd_1234",
        )
        UserProfileFactory.logout_user(browser=self.browser)

        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//button[@name='logout']"))
        )

        self.assertTrue(
            EC.element_to_be_clickable((By.XPATH, "//button[@name='login']"))
        )

    def test_change_password(self):
        UserProfileFactory.create_user(
            username="test_user", password="super_secret_pwd_1234"
        )
        UserProfileFactory.login_user(
            browser=self.browser,
            live_server_url=self.live_server_url,
            username="test_user",
            password="super_secret_pwd_1234",
        )
        UserProfileFactory.create_profile_for_test_user(username="test_user")
        UserProfileFactory.go_to_user_profile(browser=self.browser)

        change_pwd_btn = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//a[@name='change_pwd_btn']"))
        )
        self.browser.execute_script(
            "arguments[0].scrollIntoView(true);", change_pwd_btn
        )
        self.browser.execute_script("arguments[0].click();", change_pwd_btn)

        change_pwd_btn = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//button[@name='change_pwd_btn']")
            )
        )

        self.browser.find_element(By.XPATH, "//input[@name='old_password']").send_keys(
            "super_secret_pwd_1234"
        )
        self.browser.find_element(By.XPATH, "//input[@name='new_password1']").send_keys(
            "new_secret_pwd_6789"
        )
        self.browser.find_element(By.XPATH, "//input[@name='new_password2']").send_keys(
            "new_secret_pwd_6789"
        )

        self.browser.execute_script(
            "arguments[0].scrollIntoView(true);", change_pwd_btn
        )
        self.browser.execute_script("arguments[0].click();", change_pwd_btn)

        WebDriverWait(self.browser, 10).until(EC.url_changes(self.browser.current_url))

        self.assertEqual(
            self.browser.find_element(By.CLASS_NAME, "alert").text,
            "Your password was successfully updated!",
        )

        UserProfileFactory.logout_user(browser=self.browser)
        UserProfileFactory.login_user(
            browser=self.browser,
            live_server_url=self.live_server_url,
            username="test_user",
            password="new_secret_pwd_6789",
        )

        WebDriverWait(self.browser, 10).until(EC.url_changes(self.browser.current_url))

        expected_url = self.live_server_url + reverse("tweet_home")
        self.assertEqual(self.browser.current_url, expected_url)
