from django.urls import path
from django.contrib.auth import views as auth_views

from . import views
from .views import RegistrationView

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', RegistrationView.as_view(), name='register'),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
]