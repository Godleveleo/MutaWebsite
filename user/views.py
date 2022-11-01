# -*- encoding: utf-8 -*-
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
# from .forms import LoginForm, SignUpForm
from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import loader
from django.urls import reverse
from myclasses.forms import *
from django.contrib.auth.models import User
from utilidades.formularios import logueado
from django.contrib import messages
from datetime import datetime
from utilidades import formularios

def home():
    pass

def CerrarSesion(request):
    logout(request)
    return redirect("login")

def login_view(request):
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
                    # if user.groups.filter(name='manager').exists():
                                                       
                    return redirect("/")
                    # else:
                    #     msg = 'Credenciales invalidas'

                else:
                    return redirect("/")


            else:
                msg = 'Credenciales invalidas'
        else:
            msg = 'Error en el formulario'

    return render(request, "app/accounts/login.html", {"form": form, "msg": msg})



def register_user(request):
    msg = None
    success = False

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)
            UsersMetadata.objects.create(user_id = user.id)
            my_group = Group.objects.get(name='manager') 
            my_group.user_set.add(user.id)
            msg = 'Usuario creado de manera Existosa ¡BIENVENID@!'
            success = True
            return redirect("/login/")
        

        else:            
            msg = 'Lo siento, los datos ingresados no son validos'
            
    else:
        form = SignUpForm()

    return render(request, "app/accounts/register.html", {"form": form, "msg": msg, "success": success})