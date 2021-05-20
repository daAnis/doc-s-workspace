from django.urls import path

from . import views

urlpatterns = [
    path('wards/<int:ward>/<int:record_id>/prescription/delete/<int:pr_id>/', views.prescription_delete, name='prescription_delete'),
    path('wards/<int:ward>/<int:record_id>/prescription/update/<int:pr_id>/', views.prescription_update, name='prescription_update'),
    path('wards/<int:ward>/<int:record_id>/prescription/create/', views.prescription_create, name='prescription_create'),
    path('wards/<int:ward>/<int:record_id>/prescription/', views.prescription, name='prescription'),
    path('wards/<int:ward>/<int:record_id>/observation/bpp/delete/<int:bpp_id>/', views.bpp_delete, name='bpp_delete'),
    path('wards/<int:ward>/<int:record_id>/observation/bpp/update/<int:bpp_id>/', views.bpp_update, name='bpp_update'),
    path('wards/<int:ward>/<int:record_id>/observation/bpp/create/', views.bpp_create, name='bpp_create'),
    path('wards/<int:ward>/<int:record_id>/observation/temp/create/', views.temp_create, name='temp_create'),
    path('wards/<int:ward>/<int:record_id>/observation/temp/get/', views.temp_get, name='temp_get'),
    path('wards/<int:ward>/<int:record_id>/observation/', views.observation, name='observation'),
    path('wards/<int:ward>/<int:record_id>/examination/delete/<int:exam_id>/', views.examination_delete, name='examination_delete'),
    path('wards/<int:ward>/<int:record_id>/examination/update/<int:exam_id>/', views.examination_update, name='examination_update'),
    path('wards/<int:ward>/<int:record_id>/examination/create/', views.examination_create, name='examination_create'),
    path('wards/<int:ward>/<int:record_id>/examination/', views.examination, name='examination'),
    path('wards/<int:ward>/<int:record_id>/', views.record, name='record'),
    path('wards/<int:ward>/', views.records_in_ward, name='records_in_ward'),
    path('wards/', views.wards, name='wards'),
    path('', views.index, name='index'),
]