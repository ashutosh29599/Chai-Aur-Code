from django.urls import reverse

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

from django.contrib.auth.models import User

from profiles.models import Profile

from .utils import scroll_and_click


class UserProfileFactory:
    @staticmethod
    def create_user(username='test_user', password='super_secret_pwd_1234', email='test_user@domain.com'):
        User.objects.create_user(username=username, password=password, email=email)

    @staticmethod
    def create_profile_for_test_user(username='test_user'):
        user = User.objects.get(username=username)
        Profile.objects.create(user=user, email=user.email)

    @staticmethod
    def set_test_user_name(username='test_user', first_name='Test', last_name='User'):
        profile = Profile.objects.get(user=User.objects.get(username=username).id)
        profile.first_name = first_name
        profile.last_name = last_name
        profile.save()
    
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

    @staticmethod
    def create_posts_from_multiple_users_for_sorting(browser, live_server_url, sort_by):
        UserProfileFactory.create_user(
            username='a_test_user', password='super_secret_pwd_1234', email='a_test_user@domain.com'
        )
        UserProfileFactory.login_user(browser=browser, live_server_url=live_server_url,
                                      username='a_test_user', password='super_secret_pwd_1234')
        PostsFactory.create_a_post(browser=browser, post_text='This post is by a_test_user!')

        UserProfileFactory.create_user(
            username='b_test_user', password='super_secret_pwd_1234', email='b_test_user@domain.com'
        )
        UserProfileFactory.login_user(browser=browser, live_server_url=live_server_url,
                                      username='b_test_user', password='super_secret_pwd_1234')
        PostsFactory.create_a_post(browser=browser, post_text='This post is by b_test_user!')

        WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//p[@name='post_text']"))
        )

        sort_by_options = browser.find_element(By.NAME, 'sort_by')
        sort_by_options = Select(sort_by_options)

        sort_by_options.select_by_value(sort_by)

        WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.ID, 'posts-container'))
        )

        posts = browser.find_elements(By.NAME, 'post_text')
        posts = [post.text for post in posts]

        return posts

    @staticmethod
    def create_users_and_get_them_back_after_sorting_from_users_page(browser, live_server_url, sort_by):
        UserProfileFactory.create_user(
            username='a_test_user', password='super_secret_pwd_1234', email='a_test_user@domain.com'
        )
        UserProfileFactory.create_profile_for_test_user(username='a_test_user')
        UserProfileFactory.set_test_user_name(username='a_test_user', first_name='A. Test', last_name='User')

        UserProfileFactory.create_user(
            username='b_test_user', password='super_secret_pwd_1234', email='test_b_user@domain.com'
        )
        UserProfileFactory.create_profile_for_test_user(username='b_test_user')
        UserProfileFactory.set_test_user_name(username='b_test_user', first_name='B. Test', last_name='User')

        browser.get(live_server_url + reverse('users'))
        
        sort_by_options = browser.find_element(By.NAME, 'sort_by_user')
        sort_by_options = Select(sort_by_options)

        sort_by_options.select_by_value(sort_by)

        WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.ID, 'posts-container-users'))
        )

        users = browser.find_elements(By.XPATH, "//h5[@class='card-title']")
        users = [user.text for user in users]

        return users
