# -*- encoding: utf-8 -*-
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm, SignUpForm
from django import template
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import loader
from django.urls import reverse
from myclasses.forms import *
from django.contrib.auth.models import User
from utilidades.formularios import logueado
from django.contrib import messages
from datetime import datetime, date, timedelta
from utilidades import formularios
from django.contrib.auth.models import Group
from django.utils.timezone import utc
import datetime

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
                    if user.groups.filter(name='manager').exists():                                                      
                                            return redirect("/")
                    else:
                         msg = 'Credenciales invalidas'

                else:
                    return redirect("/")


            else:
                msg = 'Credenciales invalidas'
        else:
            msg = 'Error en el formulario'

    return render(request, "app/accounts/login.html", {"form": form, "msg": msg})



def register(request):
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


@login_required(login_url='login')
@user_passes_test(formularios.is_member, login_url='login')
def home(request):
    return render(request, 'app/home/user.html')

##### seccion gimnasio (agregar/listar/editar/eliminar/validaciones)######

@login_required(login_url='login')
@user_passes_test(formularios.is_member, login_url='login')
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


@login_required(login_url='login')
@user_passes_test(formularios.is_member, login_url='login')
def box_add(request):
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
                    Administradores.objects.create(comunidad_id = save.id, nombre_id=userid)                    
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
                    Administradores.objects.create(comunidad_id = save.id, nombre_id=userid)
                    messages.add_message(request, messages.SUCCESS, f"Se agrego su Gimnasio existosamente")           
                    return HttpResponseRedirect("/gym/")
            else:
                messages.add_message(request, messages.WARNING, f"Lo siento, Solo puedes registrar un Gimnasio")
                return HttpResponseRedirect("/gym/")               
              

    else:
        form = Boxform_add()          
    datos = Box.objects.filter(user_creador__exact = userid)   
    return render(request,'app/home/gym/gym.html',{"form": form, "msg": msg, 'datos':datos } )

@login_required(login_url='login')
@user_passes_test(formularios.is_member, login_url='login')   
def delete_gym(request,id):
    dato = get_object_or_404(Box, id=id)
    datoPerfil = get_object_or_404(Administradores, comunidad_id = id)
    datoPerfil.delete()
    dato.delete()
    messages.success(request, "Eliminado exitosamente")
    return redirect(to='/gym/')

@login_required
@user_passes_test(formularios.is_member, login_url='login')
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

@login_required(login_url='login')
@user_passes_test(formularios.is_member, login_url='login')
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
    

@login_required(login_url='login')
@user_passes_test(formularios.is_member, login_url='login')
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
                    comunidad = Administradores.objects.filter(nombre_id = id_u).first()
                    save.titulo = titulo
                    save.disciplina = disciplina
                    save.horario = horario
                    save.precio = precio
                    save.cantidad_clases = cantidad_clases
                    save.user_creador = id_u
                    save.comunidad_id = comunidad.comunidad_id                  
                    save.save()
                    messages.add_message(request, messages.SUCCESS, f"Se agrego su PLAN existosamente")           
                    return HttpResponseRedirect("/homeplan/")
    else:
        form = Planform_add()       
       
    return render(request,'app/home/planes/planes.html',{"form": form, })
    
@login_required(login_url='login')
@user_passes_test(formularios.is_member, login_url='login')
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

@login_required(login_url='login')
@user_passes_test(formularios.is_member, login_url='login')    
def delete_plan(request,id):
    dato = get_object_or_404(Planes, id=id)
    dato.delete()
    messages.success(request, "Eliminado exitosamente")
    return redirect(to='/homeplan/')


########## clases #######
@login_required(login_url='login')
@user_passes_test(formularios.is_member, login_url='login')
def home_clases(request):
    estado = True
    datos = None
    active = 0
    userid = request.user.id
    
    validador = Clases.objects.filter(user_creador__exact = userid).count()    
    if validador == 0:
        estado = False
        messages.add_message(request, messages.WARNING, f"No tienes CLASES creadas para tu comunidad..")
    else:
        datos = Clases.objects.filter(user_creador__exact = userid)    
    return render(request,'app/home/clases/home_clases.html',{'datos':datos, 'estado':estado} )

@login_required(login_url='login')
@user_passes_test(formularios.is_member, login_url='login')
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
                    messages.add_message(request, messages.SUCCESS, f"Se agrego la clase: {save.descripcion} existosamente")           
                    return HttpResponseRedirect("/homeclases/")
    else:
        form = Clasesform_add()       
       
    return render(request,'app/home/clases/clases.html',{"form": form, })


@login_required(login_url='login')
@user_passes_test(formularios.is_member, login_url='login')
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
         if formularios.estado_reserva(id):
            messages.add_message(request, messages.WARNING, f" !No se puede editar¡ Existe reserva activa con la clase: {clas.descripcion}  ") 
            return HttpResponseRedirect("/homeclases/")

    form = Clasesform_add(request.POST  or None, instance=clas)
    if form.is_valid() :
        form.save()
        if formularios.existeclaseActiva(id):
                update = Reserva_estado.objects.filter(clase_id__exact=id).first()
                update.cupo = clas.cupo
                update.save()
                messages.add_message(request, messages.SUCCESS, f"Se modifico su CLASES existosamente")           
        return HttpResponseRedirect("/homeclases/")
        
                    

    return render(request,'app/home/clases/clasesedit.html',{'clas':clas, 'form':form})

@login_required(login_url='login')
@user_passes_test(formularios.is_member, login_url='login')   
def delete_clases(request,id):
    if formularios.reserva_clase(id):
            messages.add_message(request, messages.WARNING, f" !No se puede Eliminar¡ Existe reserva activa con la clase ") 
            return HttpResponseRedirect("/homeclases/")
    else:

        dato = get_object_or_404(Clases, id=id)
        dato.delete()
        messages.success(request, "Clase eliminada exitosamente")
        return redirect(to='/homeclases/')


#### reservas ###

@login_required(login_url='login')
@user_passes_test(formularios.is_member, login_url='login')
def home_reserva(request): 
    estado = True
    datos = None    
    userid = request.user.id
    
    validador = Reserva_estado.objects.filter(user_creador__exact = userid).count()    
    if validador == 0:
        estado = False
        messages.add_message(request, messages.WARNING, f"No tienes Reservas activas para tu comunidad..")
    else:
        if request.method == "POST":
            fecha = request.POST['fecha']                           
            datos = Reserva_estado.objects.filter(user_creador__exact = userid, Fecha__contains=fecha)
    
    fecha = formularios.listaFechas(userid)
    return render(request,'app/home/reservas/home_reserva.html',{'datos':datos, 'estado':estado, 'fechas':fecha} )

@login_required(login_url='login')
@user_passes_test(formularios.is_member, login_url='login')
def reserva_add(request):   
    hoy = date.today()
    unDia = hoy + timedelta(days=1)
    dosDia = hoy + timedelta(days=2)
    tresDia = hoy + timedelta(days=3)
    cuatroDia = hoy + timedelta(days=4)
    cincoDia = hoy + timedelta(days=5)
    seisDia = hoy + timedelta(days=6)
    sieteDia = hoy + timedelta(days=7)   
    userid = request.user.id    
    comunidad = Box.objects.filter(user_creador = userid ).first()       
    clases = Clases.objects.filter(user_creador = userid )      
    if request.method == 'POST':                        
        form = Reservaform_add(request.POST or None)        
        if form.is_valid() :            
                    data = form.cleaned_data       
                    clase = data['clase']              
                    fechas = eval(data['fecha'])
                    id_u = request.user.id                    
                    cupototal = formularios.get_clases_cuportotal(clase)                                                 
                    for fecha in fechas:                        
                        save = Reserva_estado()
                        save.clase_id = clase
                        save.comunidad_id = comunidad.id
                        save.estado = True 
                        save.cupo = cupototal[0]                    
                        save.user_creador = id_u
                        save.Fecha = fecha                        
                        if not Reserva_estado.objects.filter(Fecha = fecha, clase_id__exact=clase).exists():
                            save.save()                            
                    
                        else:
                            messages.add_message(request, messages.WARNING, f"Ya tienes la clase activa en esa fecha")           
                            return HttpResponseRedirect("/reservaadd/")

                    messages.add_message(request, messages.SUCCESS, f"Se activo la reserva de la clase")           
                    return HttpResponseRedirect("/homereservas/")
                                              
        
    else:
        form = Reservaform_add()       
       
    return render(request,'app/home/reservas/reserva.html',
                {
                "form": form,
                "comunidad":comunidad,
                "clase":clases, 'hoy':hoy,
                'undia':unDia,
                'dosdia':dosDia,
                'tresdia':tresDia,
                'cuatrodia':cuatroDia,
                'cincodia':cincoDia,
                'seisdia':seisDia}
                )


@login_required(login_url='login')
@user_passes_test(formularios.is_member, login_url='login')   
def delete_clase_activa(request,id):
        dato = get_object_or_404(Reserva_estado, id=id)
        dato.delete()
        messages.success(request, "Reserva eliminada exitosamente")
        return redirect(to='/homereservas/')


   

@login_required(login_url='login')
@user_passes_test(formularios.is_member, login_url='login')    
def diseno_modal(request, id,clase):
    
    consulta = Reserva_activa.objects.filter(reserva_id__exact = id) 
        
    
    return render(request, 'app/home/modal/modal.html', {'consulta':consulta, 'clase':clase})


## alumnos ##

@login_required(login_url='login')
@user_passes_test(formularios.is_member, login_url='login')
def home_alumnos(request):
    user = request.user.id
    alumnos = None
    if formularios.existePerfil(user) > 0:
        alumnos = Perfil.objects.filter(comunidad_id = formularios.get_comunidad(user))
   
    return render(request,'app/home/alumnos/alumnos.html',{'alumnos':alumnos} )

@login_required(login_url='login')
@user_passes_test(formularios.is_member, login_url='login')    
def edit_perfil_modal(request, id, alumno):
    user = request.user.id    
    alumnos = Perfil.objects.filter(comunidad_id = formularios.get_comunidad(user), nombre_id = alumno)       
    perfil = get_object_or_404(Perfil, pk=id)
    form = PerfilAlumnoform(request.POST  or None, instance=perfil)
                         
    return render(request, 'app/home/alumnos/edit-perfil-modal.html', {'alumnos':alumnos, 'form':form, 'id':id })

def edit_plan_alumno_modal(request, id):
    perfil = get_object_or_404(Perfil, pk=id)
    form = PerfilAlumnoform(request.POST  or None, instance=perfil)
    if form.is_valid():
        plan = form.cleaned_data['plan']        
        pago = form.cleaned_data['vigencia']        
        perfil.plan_id = plan
        perfil.vigencia = pago
        perfil.save()        
    
    return redirect(to='/home-alumnos/')

