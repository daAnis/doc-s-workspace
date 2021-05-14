from django.urls import path

from . import views

urlpatterns = [
    path('wards', views.wards, name='wards'),
    path('', views.index, name='index'),
]