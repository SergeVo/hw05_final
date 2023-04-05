from django.test import Client, TestCase
from django.urls import reverse

from posts.models import Follow, Post, User


class FollowTests(TestCase):
    def setUp(self):
        self.client_auth_follower = Client()
        self.client_auth_following = Client()
        self.user_follower = User.objects.create(username='follower')
        self.user_following = User.objects.create(username='following')
        self.post = Post.objects.create(
            author=self.user_following,
            text='Тестовая запись для тестирования ленты'
        )
        self.client_auth_follower.force_login(self.user_follower)
        self.client_auth_following.force_login(self.user_following)

    def test_follow(self):
        self.client_auth_follower.get(
            reverse('posts:profile_follow',
                    kwargs={'username': self.user_following.username})
        )
        self.assertEqual(Follow.objects.all().count(), 1)

    def test_unfollow(self):
        self.client_auth_follower.get(reverse('posts:profile_follow',
                                              kwargs={'username':
                                                      self.user_following.
                                                      username}))
        self.client_auth_follower.get(reverse('posts:profile_unfollow',
                                      kwargs={'username':
                                              self.user_following.username}))
        self.assertEqual(Follow.objects.all().count(), 0)

    def test_subscription(self):
        """Запись появляется в ленте подписчиков"""
        Follow.objects.create(
            user=self.user_follower,
            author=self.user_following
        )
        response = self.client_auth_follower.get('/follow/')
        post_text_0 = response.context["page_obj"][0].text
        self.assertEqual(post_text_0, 'Тестовая запись для тестирования ленты')
        response = self.client_auth_following.get('/follow/')
        self.assertNotEqual(response, 'Тестовая запись для тестирования ленты')

    def test_add_comment(self):
        """Проверка добавления комментария"""
        self.client_auth_following.post(f'/posts/{self.post.pk}/comment/',
                                        {'text': "тестовый комментарий"},
                                        follow=True)
        response = self.client_auth_following.get(f'/posts/{self.post.pk}/')
        self.assertContains(response, 'тестовый комментарий')
        self.client_auth_following.logout()
        self.client_auth_following.post(f'/posts/{self.post.pk}/comment/',
                                        {'text': "комментарий от гостя"},
                                        follow=True)
        response = self.client_auth_following.get(f'/posts/{self.post.pk}/')
        self.assertNotContains(response, 'комментарий от гостя')
