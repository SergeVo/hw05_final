from django import forms

from .models import Post, Comment


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('group', 'text', 'image', )
        labels = {
            'group': 'Группа',
            'text': 'Текст нового поста',
        }
        help_texts = {
            'group': 'Выберите группу для вашего поста (Не обязательно)',
            'text': 'Введите текст вашего поста',
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
        labels = {
            'text': 'Текст',
        }
        help_texts = {
            'text': 'Текст комментария',
        }
