from django.urls import path

from . import views

urlpatterns = [
    path('', views.dataresources, name = 'dataresources'),
]