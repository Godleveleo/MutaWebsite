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
    path("homegym/", views.home_gym, name="home-gym"),
    path('deletegym/<id>/', views.delete_gym, name='delete-gym'), 
    path('editgym/<id>/', views.edit_gym, name='edit-gym'), 
    path("gym/", views.box_add, name="gym-add"),
    #### planes ##
    path("homeplan/", views.home_plan, name="home-plan"),
    path("planadd/", views.planes_add, name="plan-add"),
    path('editplan/<id>/', views.edit_plan, name='edit-plan'),
    path('deleteplan/<id>/', views.delete_plan, name='delete-plan'),
    #####clases ###
    path("homeclases/", views.home_clases, name="home-clases"),
    path("clasesadd/", views.clases_add, name="clases-add"),
    path("clasesedit/", views.edit_clases, name="edit-clases"),

    
    
    
]


# path("mygym/", views.box_view, name="gym-view"),
# re_path(r'^.*\.*', views.pages, name='pages'),