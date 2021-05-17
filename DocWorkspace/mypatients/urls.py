from django.urls import path

from . import views

urlpatterns = [
    path('wards/<int:ward>/<int:record_id>/prescription/', views.prescription, name='prescription'),
    path('wards/<int:ward>/<int:record_id>/observation/', views.observation, name='observation'),
    path('wards/<int:ward>/<int:record_id>/examination/', views.examination, name='examination'),
    path('wards/<int:ward>/<int:record_id>/', views.record, name='record'),
    path('wards/<int:ward>/', views.records_in_ward, name='records_in_ward'),
    path('wards/', views.wards, name='wards'),
    path('', views.index, name='index'),
]