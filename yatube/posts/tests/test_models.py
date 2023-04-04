from django.contrib.auth import get_user_model
from django.test import TestCase

from ..models import Group, Post

User = get_user_model()


class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.author = User.objects.create_user(username='TestAuthor')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test_slug',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            author=cls.author,
            text='Тестовый текст',
        )

    def test_models_have_correct_object_names(self):
        post_str = str(self.post)
        group_str = str(self.group)

        self.assertEqual(post_str, 'Тестовый текст')
        self.assertEqual(group_str, 'Тестовая группа')
