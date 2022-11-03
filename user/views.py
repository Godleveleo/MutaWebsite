# -*- encoding: utf-8 -*-
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from user.forms import *
from myclasses.models import UsersMetadata, Reserva_estado
from django import template
from django.contrib.auth.decorators import login_required,user_passes_test
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import loader
from django.urls import reverse
from django.contrib.auth.models import User
from utilidades.formularios import logueado
from django.contrib import messages
from datetime import datetime
from utilidades import formularios
from django.contrib.auth.models import Group

@login_required(login_url='login-usuario')
@user_passes_test(formularios.is_member_alumno, login_url='login-usuario')
def home_user(request):
    return render(request, 'user/home-user/indexUSER.html')

def CerrarSesion_user(request):
    logout(request)
    return redirect("login-usuario")
    
def login_user(request):
    form = LoginForm(request.POST or None)

    msg = None

    if request.method == "POST":
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)
            if user is not None:                
                login(request, user)
                if not user.is_superuser:
                    usersMetadata = UsersMetadata.objects.filter(user_id=request.user.id).get()
                    request.session['users_metadata_id'] =  usersMetadata.id
                    if user.groups.filter(name='alumnos').exists():
                                            return redirect("inicio-alumno")
                    else:
                         msg = 'Credenciales invalidas'

                else:
                    return redirect("inicio-alumno")


            else:
                msg = 'Credenciales invalidas'
        else:
            msg = 'Error en el formulario'

    return render(request, "user/acceso-usuario/login.html", {"form": form, "msg": msg})



def register_user(request):
    msg = None
    success = False

    if request.method == "POST":
        form = registroForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            comunidad = form.cleaned_data.get("comunidad")
            user = authenticate(username=username, password=raw_password)
            UsersMetadata.objects.create(user_id = user.id, comunidad_id = comunidad)
            my_group = Group.objects.get(name='alumnos') 
            my_group.user_set.add(user.id)
            msg = 'Usuario creado de manera Existosa ¡BIENVENID@!'
            success = True
            return redirect("login-usuario")
        

        else:            
            msg = 'Lo siento, los datos ingresados no son validos'
            
    else:
        form = registroForm()

    return render(request, "user/acceso-usuario/register.html", {"form": form, "msg": msg, "success": success})



#### reservas ###

@login_required(login_url='login-usuario')
@user_passes_test(formularios.is_member_alumno, login_url='login-usuario')
def home_reserva_user(request):
    estado = True
    datos = None    
    userid = request.user.id
    datosUsuario = UsersMetadata.objects.filter(user_id__exact = userid).first()   
    validador = Reserva_estado.objects.filter(comunidad_id__exact = datosUsuario.comunidad).count()    
    if validador == 0:
        estado = False
        messages.add_message(request, messages.WARNING, f"No tienes Reservas activas para tu comunidad..")
    else:
        datos = Reserva_estado.objects.filter(comunidad_id__exact = datosUsuario.comunidad)
        if request.method == 'POST':
            pass  
    return render(request,'user/reservas/reservas-user.html',{'datos':datos, 'estado':estado} )



# def reserva_add_user(request):
#     barra = None       
#     if request.method == 'POST':                        
#         form = Reservaform_user(request.POST or None)
#         if form.is_valid() :            
#                     data = form.cleaned_data       
#                     clase = data['clase']        
#                     estado = data['estado']
#                     id_u = request.user.id
#                     cupoReservado= 5
#                     cupototal = formularios.get_clases_cuportotal(clase)                   
#                     barra = formularios.porcentaje(cupototal[0],cupoReservado)                              
#                     save = Reserva_estado()
#                     save.clase_id = clase
#                     save.estado = estado 
#                     save.cupo = cupototal[0]                    
#                     save.barra_cupo = barra
#                     save.user_creador = id_u                                     
#                     save.save()
#                     messages.add_message(request, messages.SUCCESS, f"Se activo la reserva de la clase")           
#                     return HttpResponseRedirect("/homereservas/")
        
        
#     else:
#         form = Reservaform_user()       
       
#     return render(request,'app/home/reservas/reserva.html',{"form": form, })