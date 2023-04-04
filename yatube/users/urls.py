from django.contrib.auth.views import (LoginView, LogoutView,
                                       PasswordChangeDoneView)
from django.urls import path

from . import views

app_name = 'users'

urlpatterns = [
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('logout/', LogoutView.as_view(template_name='users/logged_out.html'),
         name='logout'),
    path('login/', LoginView.as_view(template_name='users/login.html'),
         name='login'),
    path('password_change/', LoginView.as_view
         (template_name='users/password_change_form.html'),
         name='password_change'),
    path('password_change_done/', PasswordChangeDoneView.as_view(),
         name='password_change_done'),
    path('auth/password_reset/', LoginView.as_view
         (template_name='users/password_reset_form.html'),
         name='password_reset'),
]
