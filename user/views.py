# -*- encoding: utf-8 -*-
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from user.forms import *
from myclasses.models import UsersMetadata, Reserva_estado, Reserva_activa
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
    b_reserva = True
    id_reservada = None 
    userid = request.user.id
    datosUsuario = UsersMetadata.objects.filter(user_id__exact = userid).first()   
    validador = Reserva_estado.objects.filter(comunidad_id__exact = datosUsuario.comunidad).count()    
    if validador == 0:
        estado = False
        messages.add_message(request, messages.WARNING, f"No tienes Reservas activas para tu comunidad..")
    else:
        datos = Reserva_estado.objects.filter(comunidad_id__exact = datosUsuario.comunidad)
        if request.method == 'GET':           
            if formularios.reserva_active(userid):
                search_id = formularios.get_reservaid(userid)
                id_reservada = search_id                              
                b_reserva = False
            else:
                b_reserva = True
                search_id = formularios.get_reservaid(userid)
                id_reservada = search_id
               
                                   
            
        
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
            now = datetime.datetime.now().replace(tzinfo=utc)
            reservaActiva.fecha = now
            add_cupo.save()            
            reservaActiva.save()          
            messages.add_message(request, messages.SUCCESS, f"Clase Reservada")   
            return redirect("reserva-clases")
        
        



    return render(request,'user/reservas/reservas-user.html',{'datos':datos, 'estado':estado, 'b_reserva':b_reserva, 'id_reservada':id_reservada} )

def delete_reserva(request,id=None):    
    userid = request.user.id
    id_reserva = Reserva_activa.objects.filter(user_id__exact=userid).first()    
    dato = get_object_or_404(Reserva_activa, reserva_id__exact=id,id__exact = id_reserva.id)
    delbarra = Reserva_estado.objects.filter(id=id).first()
    delbarra.cupo_reservado -= 1
    barra = formularios.porcentaje(delbarra.cupo,delbarra.cupo_reservado)
    delbarra.barra_cupo = barra
    delbarra.save()
    dato.delete()
    messages.warning(request, "Ya no tienes Clases reservadas")
    return redirect(to='reserva-clases')

# def reserva_add_user(request, id):
#      barra = None
#      print(id)       
#      if request.method == 'POST':
#             form = Reservaform_user(request.POST or None)
#             cupoReservado= 5
#             cupototal = formularios.get_clases_cuportotal(clase)                   
#             barra = formularios.porcentaje(cupototal[0],cupoReservado)                              
            
#             messages.add_message(request, messages.SUCCESS, f"Reserva realizada")           
#             return HttpResponseRedirect("reserva-clases")
                    
        
        
#      else:
#          form = Reservaform_user()       
      
#      return render(request,'user/reservas/reservas-user.html',{"form": form, })

