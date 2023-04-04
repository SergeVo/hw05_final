from django.test import Client, TestCase
from django.urls import reverse

from ..models import Comment, Post, User


class CommentTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.test_user = User.objects.create(username='TestUser')
        cls.post = Post.objects.create(
            text='Тестовый текст',
            author=cls.test_user,
        )
        cls.comment_url = reverse(
            'posts:add_comment', kwargs={'post_id': CommentTests.post.pk})

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.test_user)

    def test_authorized_client_can_add_comment(self):
        """Авторизированный пользователь может комментировать"""
        text_comment = 'Тестовый комментарий'
        self.authorized_client.post(CommentTests.comment_url,
                                    data={'text': text_comment}
                                    )
        comment = Comment.objects.filter(post=CommentTests.post).last()
        self.assertEqual(comment.text, text_comment)
        self.assertEqual(comment.post, CommentTests.post)
        self.assertEqual(comment.author, CommentTests.test_user)

    def test_unauthorized_client_redirect_to_login_page(self):
        """
        Неавторизированный пользователь не может комментировать
        и перенаправляется на страницу логина.
            
        """
        text_comment = {
            'text': 'Тестовый комментарий',
        }
        response = self.guest_client.post(reverse(
            'posts:add_comment', kwargs={'post_id': self.post.pk}),
            data=text_comment,
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, f'/auth/login/?next=/posts/{self.post.pk}/comment/')
        