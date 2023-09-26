from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name = 'home'),
    path('data/view', views.data_view, name = 'data_view'),
    path('upload/form/', views.model_form_upload, name = 'model_form_upload'),
    path('upload/simple/', views.simple_upload, name = 'simple_upload'),
    path('about/', views.about, name = 'about'),
]