from django.test import SimpleTestCase
from django.urls import reverse, resolve

from tweet.views import tweet_home, tweet_create, tweet_edit, tweet_delete, tweet_search, users

class PostsURLTest(SimpleTestCase):
    def test_home_url_resolves(self):
        url = reverse('tweet_home')
        self.assertEqual(resolve(url).func, tweet_home)

    def test_create_url_resolves(self):
        url = reverse('tweet_create')
        self.assertEqual(resolve(url).func, tweet_create)

    def test_edit_url_resolves(self):
        url = reverse('tweet_edit', kwargs={'tweet_id': 1})
        self.assertEqual(resolve(url).func, tweet_edit)

    def test_delete_url_resolves(self):
        url = reverse('tweet_delete', kwargs={'tweet_id': 1})
        self.assertEqual(resolve(url).func, tweet_delete)

    def test_search_url_resolves(self):
        url = reverse('tweet_search')
        self.assertEqual(resolve(url).func, tweet_search)

    def test_users_url_resolves(self):
        url = reverse('users')
        self.assertEqual(resolve(url).func, users)
