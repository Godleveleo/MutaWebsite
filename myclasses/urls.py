# -*- encoding: utf-8 -*-
from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView
from django.urls import path, re_path

urlpatterns = [
    path('', views.home, name="home"),
    path('login/', views.login_view, name="login"),
    path('register/', views.register_user, name="register"),
    path("logout/", LogoutView.as_view(), name="logout"),
    
    # re_path(r'^.*\.*', views.pages, name='pages'),
    path("gym/", views.box_add, name="gym-add"),
    
    
]
