from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('new_patient/', views.create_new_patient, name='new_p'),
    path('search_patient/', views.search_patient, name='search_p'),
    path('', views.index, name='emergency_app'),
]