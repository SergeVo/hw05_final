from django.core.cache import cache
from django.test import Client, TestCase
from django.urls import reverse

from ..models import Post, User


class CacheTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.author = User.objects.create(username='TestAuthor')
        cls.post = Post.objects.create(
            text='Тестовый текст',
            author=cls.author,
            image=None,
        )

    def setUp(self):
        self.guest_client = Client()
        cache.clear()

    def test_cache(self):
        """Тестируем кэширование"""
        response = self.client.get(reverse('posts:index'))
        cached_response_content = response.content
        Post.objects.create(text='Пост 2', author=self.author)
        response = self.client.get(reverse('posts:index'))
        self.assertEqual(cached_response_content, response.content)
        cache.clear()
        response = self.client.get(reverse('posts:index'))
        self.assertNotEqual(cached_response_content, response.content)

    def test_index_page_caches_content_for_anonymous(self):
        """Кэш контента для неавторизованного пользователя"""
        post = Post.objects.create(
            text='Текст для теста',
            author=self.author
        )
        response = self.guest_client.get(reverse('posts:index'))
        content_old = response.content
        post.delete()
        response = self.guest_client.get(reverse('posts:index'))
        self.assertEqual(response.content, content_old)
        cache.clear()
        response = self.guest_client.get(reverse('posts:index'))
        self.assertNotEqual(response.content, content_old)
