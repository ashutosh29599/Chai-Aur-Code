from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from profiles.models import Profile
from tweet.models import Tweet


class PostsHomeViewTest(TestCase):
    """
        TODO: test the sorting.
    """
    def test_home_with_default_sorting(self):
        response = self.client.get(reverse('tweet_home'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tweet_home.html')

    def test_home_ajax(self):
        response = self.client.get(reverse('tweet_home'),  HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'partials/tweet_list.html')


class PostsCreateEditDeleteTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test_user', password='super_secret_pwd_1')
        Profile.objects.create(user=self.user, email=self.user.email)

        self.client.login(username='test_user', password='super_secret_pwd_1')

    # Post Create #
    def test_create_post_GET(self):
        response = self.client.get(reverse('tweet_create'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tweet_form.html')

    def test_create_post_POST_valid_data(self):
        data = {
            'user': self.user,
            'text': 'Test Post!',   
        }

        response = self.client.post(reverse('tweet_create'), data)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Tweet.objects.count(), 1)

        self.assertRedirects(response, reverse('tweet_home'))

    def test_create_post_POST_invalid_data_text_too_long(self):
        data = {
            'user': self.user,
            'text': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aenean orci augue, dictum ac ullamcorper eu, egestas vel ante. Praesent sed efficitur tortor, in tincidunt arcu. Donec tincidunt dolor ac tortor ornare sollicitudin. Duis commodo iaculis nunc, in tempor diam. Aliquam molestie magna nibh, sit amet semper nisl bibendum sit amet. Donec dictum ex facilisis ex iaculis, at fermentum lectus tristique. Praesent ut urna suscipit odio molestie faucibus. Quisque nunc nibh, ullamcorper ut risus pharetra, aliquet suscipit leo. Aliquam gravida pretium odio hendrerit viverra. Nullam vitae libero sit amet odio pharetra iaculis. Maecenas id augue lacus. Etiam non ligula varius, volutpat dui et, condimentum arcu. Suspendisse potenti. Praesent suscipit, ligula quis vulputate tristique, eros quam aliquet mauris, sed gravida diam eros in ante. Nullam consequat sed lectus a sodales. Mauris varius leo sit amet massa bibendum condimentum. Phasellus sit amet cursus odio, non tincidunt risus. Mauris molestie mi eget lacus finibus dapibus. Sed sapien dolor, porta pharetra blandit nec, congue sit amet enim. Aenean turpis elit, ullamcorper a bibendum quis, fermentum quis nisl. Vestibulum purus odio, scelerisque vitae ultricies ac, aliquet sed diam. Sed consequat purus vel lacus tincidunt vehicula. Morbi vitae sapien in nisi maximus dapibus ac sit amet neque. Mauris lacus urna, vulputate maximus semper at, volutpat quis nunc. Sed tortor justo, faucibus condimentum gravida eget, vestibulum non nisi. Vestibulum at erat in metus egestas vehicula. Integer eget lectus in erat sagittis aliquam. Nullam vitae ornare nibh. Nunc efficitur, ipsum ut vehicula maximus, leo augue dignissim arcu, sit amet.',   
        }

        response = self.client.post(reverse('tweet_create'), data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Tweet.objects.count(), 0)

        self.assertTemplateUsed(response, 'tweet_form.html')

    def test_create_post_POST_required_fields(self):
        data = {}

        response = self.client.post(reverse('tweet_create'), data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Tweet.objects.count(), 0)

        self.assertTemplateUsed(response, 'tweet_form.html')

    # Post Edit #
    def test_edit_post_GET(self):
        data = {
            'user': self.user,
            'text': 'Test Post!',   
        }

        self.client.post(reverse('tweet_create'), data)

        post = Tweet.objects.all()[0]

        response = self.client.get(reverse('tweet_edit', kwargs={'tweet_id': post.id}))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tweet_form.html')
        
    def test_edit_post_POST_valid_data(self):
        data = {
            'user': self.user,
            'text': 'Test Post!',   
        }

        self.client.post(reverse('tweet_create'), data)
        
        updated_data = {
            'user': self.user,
            'text': 'Test Post! Editing it...',   
        }
        post = Tweet.objects.all()[0]

        response = self.client.post(reverse('tweet_edit', kwargs={'tweet_id': post.id}), updated_data)
        
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Tweet.objects.count(), 1)
        self.assertRedirects(response, reverse('tweet_home'))

        updated_post = Tweet.objects.all()[0]

        self.assertEqual(updated_post.text, updated_data['text'])

    def test_edit_post_POST_invalid_id(self):
        response = self.client.post(reverse('tweet_edit', kwargs={'tweet_id': 1}))

        self.assertEqual(response.status_code, 404)

    # Post Delete #
    def test_delete_post_GET(self):
        # Create the post to be deleted
        data = {
            'user': self.user,
            'text': 'Test Post!',   
        }

        self.client.post(reverse('tweet_create'), data)
        post = Tweet.objects.all()[0]

        response = self.client.get(reverse('tweet_delete', kwargs={'tweet_id': post.id}))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tweet_confirm_delete.html')

    def test_delete_post_POST_valid_data(self):
        # Create the post to be deleted
        data = {
            'user': self.user,
            'text': 'Test Post!',   
        }

        self.client.post(reverse('tweet_create'), data)
        post = Tweet.objects.all()[0]

        response = self.client.post(reverse('tweet_delete', kwargs={'tweet_id': post.id}))

        self.assertEqual(Tweet.objects.count(), 0)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('tweet_home'))
        
    def test_delete_post_POST_invalid_data(self):
        response = self.client.post(reverse('tweet_delete', kwargs={'tweet_id': 1}))

        self.assertEqual(response.status_code, 404)
        

class UsersViewTest(TestCase):
    def test_users_GET(self):
        response = self.client.get(reverse('users'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users.html')

    def test_users_ajax(self):
        response = self.client.get(reverse('users'), HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'partials/user_list.html')

