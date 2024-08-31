from django.contrib.auth.models import User
from django.test import LiveServerTestCase


from selenium import webdriver
from selenium.webdriver.firefox.service import Service

from profiles.models import Profile


class IntegrationTest(LiveServerTestCase):
    def setUp(self):
        gecko_driver_path = (
            "/Users/ashutosh/Desktop/Programming/Django/Chai-Aur-Tweet/geckodriver"
        )
        service = Service(executable_path=gecko_driver_path)
        # options = Options()
        # options.add_argument("-headless") 

        self.browser = webdriver.Firefox(service=service)

    def tearDown(self):
        self.browser.quit()
        User.objects.all().delete()
        Profile.objects.all().delete()
