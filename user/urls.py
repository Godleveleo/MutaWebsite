# -*- encoding: utf-8 -*-
from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView
from django.urls import path, re_path

urlpatterns = [
    path('', views.home_user, name="inicio-alumno"),
    path('login/user', views.login_user, name="login-usuario"),
    path('logout', views.CerrarSesion_user, name= 'logout-user'),
    path('registro/user', views.register_user, name="registro-usuario"),
    #### reserva de clases###
    path('reserva-clase/', views.home_reserva_user, name="reserva-clases"),
    path('deletereserva/<id>/', views.delete_reserva, name='delete-reserva'),
    

    


    
    
    
]
