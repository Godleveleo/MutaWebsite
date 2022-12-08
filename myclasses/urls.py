# -*- encoding: utf-8 -*-
from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView
from django.urls import path, re_path

urlpatterns = [
    path('', views.home, name="home"),
    path('login/', views.login_view, name="login"),
    path('register/', views.register, name="register"),
    path('logout', views.CerrarSesion, name= 'logout'),
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
    path("clasesedit/<id>/", views.edit_clases, name="edit-clases"),
    path('deleteclase/<id>/', views.delete_clases, name='delete-clases'),
    ###reserva###
    path("homereservas/", views.home_reserva, name="home-reservas"),
    path("reservaadd/", views.reserva_add, name="reserva-add"),
    path('delete-clase-activa/<id>/', views.delete_clase_activa, name='delete-reserva'),
    #####
    path('modal/<int:id>/<str:clase>', views.diseno_modal, name="diseno_modal"),
    ###alumnos##
    path("home-alumnos/", views.home_alumnos, name="Lista-alumnos"),
    path('editar-plan/<int:id>/<int:alumno>', views.edit_perfil_modal, name="modal-perfil-edit"),
    path('editar-perfil/<int:id>', views.edit_plan_alumno_modal, name="perfil-edit"),
    

    
    
]


# path("mygym/", views.box_view, name="gym-view"),
# re_path(r'^.*\.*', views.pages, name='pages'),