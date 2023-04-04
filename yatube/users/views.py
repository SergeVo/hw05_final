from django.contrib.auth.views import (LogoutView, PasswordChangeDoneView,
                                       PasswordChangeView)
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import CreationForm


class SignUp(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy('posts:index')
    template_name = 'users/signup.html'


class PasswordChange(PasswordChangeView):
    form_class = CreationForm
    template_name = 'users/password_change_form.html'


class PasswordChangeDone(PasswordChangeDoneView):
    template_name = '/password_change_done.html'


class Logout(LogoutView):
    template_name = 'users/logged_out.html'
