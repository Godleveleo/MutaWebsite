# -*- encoding: utf-8 -*-
from tkinter.ttk import Progressbar
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from .forms import LoginForm, SignUpForm
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
                    return redirect("/")
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

##### seccion gimnasio (agregar/listar/editar/eliminar/validaciones)######

@login_required
def home_gym(request):
    estado = True
    datos = None
    userid = request.user.id
    validador = Box.objects.filter(user_creador__exact = userid).count()    
    if validador == 0:
        estado = False
        messages.add_message(request, messages.WARNING, f"No tienes nada creado aun.. ! Vamos Animate !")
    else:
        datos = Box.objects.filter(user_creador__exact = userid)    
    return render(request,'app/home/gym/home_gym.html',{'datos':datos, 'estado':estado} )


@login_required
def box_add(request):
    context= {}
    datos = None
    logo = None
    msg = None    
    userid = request.user.id
    limit = Box.objects.filter(user_creador__exact = userid).count()
    if request.method == 'POST':        
        form = Boxform_add(request.POST, request.FILES)
        if request.POST['foto']=='vacio':
            logo = "logo/sinfoto.png"
            max = 1
            if limit < max:
                if form.is_valid() :
                    data = form.cleaned_data       
                    box = data['box']
                    ubicacion = data['ubicacion']
                    descripcion = data['descripcion']        
                    id_u = request.user.id            
                    save = Box()
                    save.box = box
                    save.ubicacion = ubicacion
                    save.logo = logo
                    save.descripcion = descripcion
                    save.user_creador = id_u                  
                    save.save()
                    messages.add_message(request, messages.SUCCESS, f"Se agrego su Gimnasio existosamente")           
                    return HttpResponseRedirect("/gym/")
            else:
                messages.add_message(request, messages.WARNING, f"Lo siento, Solo puedes registrar un Gimnasio")
                return HttpResponseRedirect("/gym/")
                    
        else:
            logo = request.FILES['logo']
            max = 1
            if limit < max:
                if form.is_valid() :
                    data = form.cleaned_data       
                    box = data['box']
                    ubicacion = data['ubicacion']
                    descripcion = data['descripcion']        
                    id_u = request.user.id            
                    save = Box()
                    save.box = box
                    save.ubicacion = ubicacion
                    save.logo = logo
                    save.descripcion = descripcion
                    save.user_creador = id_u                  
                    save.save()
                    messages.add_message(request, messages.SUCCESS, f"Se agrego su Gimnasio existosamente")           
                    return HttpResponseRedirect("/gym/")
            else:
                messages.add_message(request, messages.WARNING, f"Lo siento, Solo puedes registrar un Gimnasio")
                return HttpResponseRedirect("/gym/")               
              

    else:
        form = Boxform_add()          
    datos = Box.objects.filter(user_creador__exact = userid)   
    return render(request,'app/home/gym/gym.html',{"form": form, "msg": msg, 'datos':datos } )

@login_required    
def delete_gym(request,id):
    dato = get_object_or_404(Box, id=id)
    dato.delete()
    messages.success(request, "Eliminado exitosamente")
    return redirect(to='/gym/')

@login_required
def edit_gym(request,id=None):
    context= {}        
    gym = Box.objects.get(pk=id)
    user = request.user
    userid = int(request.user.id)
    idbox = int(gym.user_creador)   
    if request.method == "GET":
         if id:                
            if not user.is_superuser:
                if idbox != userid:
                    html_template = loader.get_template('app/home/page-404.html')
                    return HttpResponse(html_template.render(context, request))



    form = Boxform_add(request.POST  or None, instance=gym)              
    if request.method == "POST":
        validar = request.POST['foto']
        if validar == 'vacio':
            logo = gym.logo
            if form.is_valid():
                form.save()
                messages.add_message(request, messages.SUCCESS, f"Se realizo la modificacion con exito")           
                return HttpResponseRedirect("/gym/")        
        else:                       
            logo = request.FILES['logo']                       
            if form.is_valid():
                gym.logo
                gym.logo = logo
                gym.save()                
                form.save()           
                messages.add_message(request, messages.SUCCESS, f"Se realizo la modificacion con exito")           
                return HttpResponseRedirect("/gym/")  
        
    return render(request,'app/home/gym/gymedit.html',{'gym':gym, 'form':form})

##### fin gimnasio ####


##### planes de gimnasio creado #########

@login_required
def home_plan(request):
    estado = True
    datos = None
    userid = request.user.id
    validador = Planes.objects.filter(user_creador__exact = userid).count()    
    if validador == 0:
        estado = False
        messages.add_message(request, messages.WARNING, f"No tienes planes creados para tu comunidad..")
    else:
        datos = Planes.objects.filter(user_creador__exact = userid)    
    return render(request,'app/home/planes/home-plan.html',{'datos':datos, 'estado':estado} )
    

@login_required
def planes_add(request):       
    if request.method == 'POST':        
        form = Planform_add(request.POST or None)
        if form.is_valid() :
                    data = form.cleaned_data       
                    titulo = data['titulo']
                    disciplina = data['disciplina']
                    horario = data['horario']        
                    precio = data['precio']        
                    cantidad_clases = data['cantidad_clases']        
                    id_u = request.user.id                                
                    save = Planes()
                    save.titulo = titulo
                    save.disciplina = disciplina
                    save.horario = horario
                    save.precio = precio
                    save.cantidad_clases = cantidad_clases
                    save.user_creador = id_u                  
                    save.save()
                    messages.add_message(request, messages.SUCCESS, f"Se agrego su PLAN existosamente")           
                    return HttpResponseRedirect("/homeplan/")
    else:
        form = Planform_add()       
       
    return render(request,'app/home/planes/planes.html',{"form": form, })
    
@login_required
def edit_plan(request,id=None):
    context= {}        
    plan = Planes.objects.get(pk=id)
    user = request.user
    userid = int(request.user.id)
    idplan = int(plan.user_creador)   
    if request.method == "GET":
         if id:                
            if not user.is_superuser:
                if idplan != userid:
                    html_template = loader.get_template('app/home/page-404.html')
                    return HttpResponse(html_template.render(context, request))

    form = Planform_add(request.POST  or None, instance=plan)
    if form.is_valid() :
        form.save()
        messages.add_message(request, messages.SUCCESS, f"Se modifico su PLAN existosamente")           
        return HttpResponseRedirect("/homeplan/")
        
                    

    return render(request,'app/home/planes/edit-plan.html',{'plan':plan, 'form':form})

@login_required    
def delete_plan(request,id):
    dato = get_object_or_404(Planes, id=id)
    dato.delete()
    messages.success(request, "Eliminado exitosamente")
    return redirect(to='/homeplan/')


########## clases #######
@login_required
def home_clases(request):
    estado = True
    disable = None
    datos = None
    active = 0
    userid = request.user.id
    if request.method == "GET":
        reserva_activa = Reserva_estado.objects.all().count()        
        if reserva_activa == active:
            disable = False            
    validador = Clases.objects.filter(user_creador__exact = userid).count()    
    if validador == 0:
        estado = False
        messages.add_message(request, messages.WARNING, f"No tienes CLASES creadas para tu comunidad..")
    else:
        datos = Clases.objects.filter(user_creador__exact = userid)    
    return render(request,'app/home/clases/home_clases.html',{'datos':datos, 'estado':estado, 'disable':disable} )

@login_required
def clases_add(request):       
    if request.method == 'POST':                
        form = Clasesform_add(request.POST or None)
        if form.is_valid() :            
                    data = form.cleaned_data       
                    descripcion = data['descripcion']
                    inicio = data['inicioClase']
                    termino = data['terminoClase']        
                    duracion = data['duracion']        
                    modalidad = data['modalidad']        
                    cupo = data['cupo']        
                    id_u = request.user.id                                                   
                    save = Clases()                    
                    save.descripcion = descripcion
                    save.inicioClase = inicio
                    save.terminoClase = termino
                    save.duracion = duracion
                    save.modalidad = modalidad
                    save.cupo = cupo
                    save.user_creador = id_u                  
                    save.save()
                    messages.add_message(request, messages.SUCCESS, f"Se agrego la CLASE existosamente")           
                    return HttpResponseRedirect("/homeclases/")
    else:
        form = Clasesform_add()       
       
    return render(request,'app/home/clases/clases.html',{"form": form, })


@login_required
def edit_clases(request,id=None):
    context= {}
    clas = Clases.objects.get(pk=id)     
    user = request.user
    userid = int(request.user.id)
    idclas =  int(clas.user_creador)     
    if request.method == "GET":
         if id:                
            if not user.is_superuser:
                if idclas != userid:
                    html_template = loader.get_template('app/home/page-404.html')
                    return HttpResponse(html_template.render(context, request))

    form = Clasesform_add(request.POST  or None, instance=clas)
    if form.is_valid() :
        form.save()
        messages.add_message(request, messages.SUCCESS, f"Se modifico su CLASES existosamente")           
        return HttpResponseRedirect("/homeclases/")
        
                    

    return render(request,'app/home/clases/clasesedit.html',{'clas':clas, 'form':form})

@login_required    
def delete_clases(request,id):
    dato = get_object_or_404(Clases, id=id)
    dato.delete()
    messages.success(request, "Eliminado exitosamente")
    return redirect(to='/homeclases/')


#### reservas ###

@login_required
def home_reserva(request):
    estado = True
    datos = None
    datos = Reserva_estado.objects.all()
    userid = request.user.id
    validador = Reserva_estado.objects.filter(user_creador__exact = userid).count()    
    if validador == 0:
        estado = False
        messages.add_message(request, messages.WARNING, f"No tienes Reservas activas para tu comunidad..")
    else:
        datos = Reserva_estado.objects.all()   
    return render(request,'app/home/reservas/home_reserva.html',{'datos':datos, 'estado':estado} )

@login_required
def reserva_add(request):
    barra = None       
    if request.method == 'POST':                        
        form = Reservaform_add(request.POST or None)
        if form.is_valid() :            
                    data = form.cleaned_data       
                    clase = data['clase']        
                    estado = data['estado']
                    id_u = request.user.id
                    cupototal = formularios.get_clases_cuportotal(clase)
                    cupoReservado = 8
                    barra = formularios.porcentaje(cupototal[0],cupoReservado)                              
                    save = Reserva_estado()
                    save.clase_id = clase
                    save.estado = estado 
                    save.cupo = cupototal[0]
                    save.cupo_reservado = cupoReservado
                    save.barra_cupo = barra
                    save.user_creador = id_u                                     
                    save.save()
                    messages.add_message(request, messages.SUCCESS, f"Se agrego la reserva existosamente")           
                    return HttpResponseRedirect("/homereservas/")
        
        
    else:
        form = Reservaform_add()       
       
    return render(request,'app/home/reservas/reserva.html',{"form": form, })