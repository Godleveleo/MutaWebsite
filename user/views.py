# -*- encoding: utf-8 -*-
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from user.forms import *
from myclasses.models import UsersMetadata, Reserva_estado, Reserva_activa, Perfil
from django import template
from django.contrib.auth.decorators import login_required,user_passes_test
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import loader
from django.urls import reverse
from django.contrib.auth.models import User
from utilidades.formularios import logueado
from django.contrib import messages
import datetime
from utilidades import formularios
from django.contrib.auth.models import Group
from django.utils.timezone import utc



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
            Perfil.objects.create(nombre_id = user.id, comunidad_id = comunidad)
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
    comunidad =datosUsuario.comunidad_id   
    validador = Reserva_estado.objects.filter(comunidad_id__exact = datosUsuario.comunidad).count()    
    if validador == 0:
        estado = False
        messages.add_message(request, messages.WARNING, f"No hay Clases activas en tu comunidad..")
    else:
        if request.method == "POST":
            fecha = request.POST['fecha']
            datos = Reserva_estado.objects.filter(comunidad_id__exact = comunidad, Fecha__contains=fecha)    
    reserva_usuario = Reserva_activa.objects.filter(user_id__exact = userid).filter(comunidad__exact=comunidad).first()
    reserva_usuario_principal = Reserva_activa.objects.filter(user_id__exact = userid).filter(comunidad__exact=comunidad)
    clases_activasPorComunidad = formularios.FiltroFechasUser(comunidad)
    perfil_alumno = Perfil.objects.filter(nombre_id = userid).first()           
                                

    return render(request,'user/reservas/reservas-user.html',{'datos':datos, 'estado':estado, 'datosComunidad':clases_activasPorComunidad, 'reservasActivas':reserva_usuario, 'listarResevas':reserva_usuario_principal, 'perfil':perfil_alumno} )

def delete_reserva(request,id,rid):    
    userid = request.user.id 
    id_reserva = Reserva_activa.objects.filter(user_id__exact=userid).first()    
    dato = get_object_or_404(Reserva_activa, reserva_id__exact=id,id__exact=rid)
    delbarra = Reserva_estado.objects.filter(id=id).first()
    delbarra.cupo_reservado -= 1
    barra = formularios.porcentaje(delbarra.cupo,delbarra.cupo_reservado)
    delbarra.barra_cupo = barra
    delbarra.save()
    dato.delete()
    messages.warning(request, f"Reserva fecha: {id_reserva.fecha} de {id_reserva.reserva.clase.descripcion} eliminada")
    return redirect(to='reserva-clases')

def add_reserva(request):
    userid = request.user.id
    if request.method == 'POST':
                    cupo_id = request.POST['id']            
                    add_cupo = Reserva_estado.objects.filter(id__exact = cupo_id).first()
                    add_cupo.cupo_reservado += 1
                    barra = formularios.porcentaje(add_cupo.cupo,add_cupo.cupo_reservado)
                    add_cupo.barra_cupo = barra
                    reservaActiva = Reserva_activa()
                    reservaActiva.user_id = userid
                    reservaActiva.reserva_id = add_cupo.id
                    reservaActiva.comunidad = add_cupo.comunidad_id
                    reservaActiva.fecha = add_cupo.Fecha
                    add_cupo.save()            
                    reservaActiva.save()          
                    messages.add_message(request, messages.SUCCESS, f"Clase de {add_cupo.clase.descripcion} Reservada")   
                    return redirect("reserva-clases")    

## inicio Usuario (ALumno)        
@login_required(login_url='login-usuario')
@user_passes_test(formularios.is_member_alumno, login_url='login-usuario')
def home_user(request):
    userid = request.user.id
    perfil_alumno = Perfil.objects.filter(nombre_id = userid).first()
    
    return render(request, 'user/home-user/indexUSER.html', {'perfil':perfil_alumno})