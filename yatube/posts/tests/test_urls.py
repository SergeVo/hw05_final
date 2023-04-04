from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.core.cache import cache

from ..models import Group, Post, Comment, Follow

User = get_user_model()


class PostURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        """Создание записи в БД для проверки адреса user/test-slug/"""
        cls.author = User.objects.create(username='TestAuthor')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test_slug',
            description='Тестовое описание'
        )
        cls.post = Post.objects.create(
            author=cls.author,
            text='Тестовый текст',
            group=cls.group
        )

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.author)
        cache.clear()

    def test_guest_urls(self):
        """Проверяем доступность публичных страниц для всех"""
        urls_names = {
            '/': 200,
            '/group/test_slug/': 200,
            '/profile/TestAuthor/': 200,
            f'/posts/{self.post.pk}/': 200,
            '/unexisting_page/': 404,
        }
        for address, status in urls_names.items():
            with self.subTest(address=address):
                response = self.guest_client.get(address)
                self.assertEqual(response.status_code, status)

    def test_autorized_urls(self):
        """Проверяем доступность непубличных страниц авторизованному автору"""
        urls_names = {
            f'/posts/{self.post.pk}/edit/': 200,
            '/create/': 200,
        }
        for address, status in urls_names.items():
            with self.subTest(address=address):
                response = self.authorized_client.get(address)
                self.assertEqual(response.status_code, status)

    def test_url_to_template(self):
        """Проверка соответсвия url и template"""
        urls_template = {
            '/': 'posts/index.html',
            '/group/test_slug/': 'posts/group_list.html',
            '/profile/TestAuthor/': 'posts/profile.html',
            f'/posts/{self.post.pk}/': 'posts/post_detail.html',
            f'/posts/{self.post.pk}/edit/': 'posts/create_post.html',
            '/create/': 'posts/create_post.html',

        }
        for address, template in urls_template.items():
            with self.subTest(address=address):
                response = self.authorized_client.get(address)
                self.assertTemplateUsed(response, template)

    def test_post_edit_no_author(self):
        """Проверка редактирования поста не авторизованным
        пользователем и редирект на login"""
        response = self.guest_client.get(
            f"/posts/{self.post.pk}/edit/")
        self.assertRedirects(response, (
            f'/auth/login/?next=/posts/{self.post.id}/edit/'))
