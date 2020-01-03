from django.urls import path
from django.urls import include, path

from . import views

urlpatterns = [
    path('', views.index_view, name='index'),
]