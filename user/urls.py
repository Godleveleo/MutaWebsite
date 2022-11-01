# -*- encoding: utf-8 -*-
from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView
from django.urls import path, re_path

urlpatterns = [
    path('', views.home, name="home"),
    


    
    
    
]
