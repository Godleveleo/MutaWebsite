# -*- encoding: utf-8 -*-
from urllib import request
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import LoginForm, SignUpForm
from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from myclasses.forms import *
from django.contrib.auth.models import User
from utilidades.formularios import logueado
from django.contrib import messages

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
                usersMetadata = UsersMetadata.objects.filter(user_id=request.user.id).get()
                request.session['users_metadata_id'] =  usersMetadata.id            
                
                return redirect("/")
            else:
                msg = 'Invalid credentials'
        else:
            msg = 'Error validating the form'

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
            msg = 'Usuario creado de manera Existosa ¡BIENVENID@!'
            success = True
            return redirect("/login/")

        else:
            msg = 'Lo siento, los datos ingresados no son validos'
    else:
        form = SignUpForm()

    return render(request, "app/accounts/register.html", {"form": form, "msg": msg, "success": success})


# def pages(request):
#     context = {}
#     # All resource paths end in .html.
#     # Pick out the html file name from the url. And load that template.
#     try:

#         load_template = request.path.split('/')[-1]

#         if load_template == 'admin':
#             return HttpResponseRedirect(reverse('admin:index'))
#         context['segment'] = load_template

#         html_template = loader.get_template('app/home/' + load_template)
#         return HttpResponse(html_template.render(context, request))

#     except template.TemplateDoesNotExist:

#         html_template = loader.get_template('app/home/page-404.html')
#         return HttpResponse(html_template.render(context, request))

#     except:
#         html_template = loader.get_template('app/home/page-500.html')
#         return HttpResponse(html_template.render(context, request))



@login_required
def home(request):
    return render(request, 'app/home/index.html')


@login_required
def box_add(request):
    msg = None
    if request.method == 'POST':
        form = Boxform_add(request.POST) 
        
        if form.is_valid():
            data = form.cleaned_data                      
            
            box = data['box']
            ubicacion = data['ubicacion']
            descripcion = data['descripcion']         
            id_u = request.user.id            
            save = Box()
            save.box = box
            save.ubicacion = ubicacion
            save.descripcion = descripcion
            save.user_creador = id_u                  
            save.save()           
            return HttpResponseRedirect("/gym/")
        else:
            msg = 'Nooo, algo salio mal'

    else:
        form = Boxform_add() 
    return render(request,'app/home/gym.html',{"form": form, "msg": msg, } )

    

def box_view(request, id=None):

    if request.method == "GET":
           
        datos=Box.objects.filter(pk=id).first()

        if id:
            usr = request.user.id
            if not usr.is_superuser:
                if datos.user_creador != usr:

                    



        
   return render(request, 'app/home/gym.html', {'datos':datos})