from django.contrib.auth.models import User

from django.test import LiveServerTestCase
from django.urls import reverse

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from .factories import UserProfileFactory


class UserProfileTest(LiveServerTestCase):
    def setUp(self):
        gecko_driver_path = '/Users/ashutosh/Desktop/Programming/Django/Chai-Aur-Tweet/geckodriver'
        service = Service(executable_path=gecko_driver_path)
        # options = Options()

        self.browser = webdriver.Firefox(service=service)
    
    def tearDown(self):
        self.browser.quit()
        User.objects.all().delete()

    def test_go_to_user_profile(self):
        UserProfileFactory.create_user(username='test_user', password='super_secret_pwd_1234')
        UserProfileFactory.login_user(browser=self.browser, live_server_url=self.live_server_url,
                                      username='test_user', password='super_secret_pwd_1234')
        UserProfileFactory.create_profile_for_test_user(username='test_user')
        UserProfileFactory.go_to_user_profile(browser=self.browser)

        WebDriverWait(self.browser, 10).until(
            EC.url_changes(self.browser.current_url)
        )
        
        self.assertEqual(self.browser.title, 'Profile')

    def test_edit_profile(self):
        UserProfileFactory.create_user(username='test_user', password='super_secret_pwd_1234')
        UserProfileFactory.login_user(browser=self.browser, live_server_url=self.live_server_url,
                                      username='test_user', password='super_secret_pwd_1234')
        UserProfileFactory.create_profile_for_test_user(username='test_user')
        UserProfileFactory.go_to_user_profile(browser=self.browser)

        edit_profile_btn = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//a[@name='edit_profile_btn']"))
        )
        self.browser.execute_script("arguments[0].scrollIntoView(true);", edit_profile_btn)
        self.browser.execute_script("arguments[0].click();", edit_profile_btn)

        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.XPATH, '//h1[contains(text(), "Update your profile,")]'))
        )
        self.browser.find_element(By.NAME, 'first_name').send_keys('Test')
        self.browser.find_element(By.NAME, 'last_name').send_keys('User')
        self.browser.find_element(By.NAME, 'email').send_keys('test_user@domain.com')
        self.browser.find_element(By.NAME, 'bio').send_keys('This is the test user\'s bio!')

        update_btn = WebDriverWait(self.browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@name='update_btn']"))
        )
        self.browser.execute_script("arguments[0].scrollIntoView();", update_btn)
        self.browser.execute_script("arguments[0].click(true);", update_btn)

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

