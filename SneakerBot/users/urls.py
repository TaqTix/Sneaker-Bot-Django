from django.contrib import admin
from django.urls import include, path

from users import views

urlpatterns = [
    path('', views.login_request, name='login'),
    path('register/', views.register, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.logout_request, name='logout'), 
    path('login/', views.login, name='login' ),
]

