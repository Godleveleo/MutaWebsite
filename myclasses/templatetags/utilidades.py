from django import template
from myclasses.models import *
from datetime import datetime
from datetime import datetime ,date, timedelta

register = template.Library()


@register.filter(name='alumnoConReserva')
def alumnoConReserva(user_id):
    nombre = User.objects.filter(id__exact = user_id).first()
    primerNombre = f"{nombre.first_name} {nombre.last_name}"
    return primerNombre



@register.filter(name='existeReserva')
def existeReserva(id):    
    return Reserva_activa.objects.filter(reserva_id__exact=id).exists()
    
    
    
#######Métodos de bases de datos
@register.filter(name='existeAtributoEnProducto')
def existeAtributoEnProducto(producto_id, atributo_id):
    datos = ProdcutoAtributo.objects.filter(producto_id=producto_id).filter(atributo_id=atributo_id).count()
    if datos ==0:
        return ''
    else:
        return 'checked=true'


@register.filter(name='getMetadata')
def getMetadata(n):
    datos=Keywords.objects.get()
    lista=[datos.tiktok_redsocial, datos.correo_contacto, datos.correo_sugerencias_reclamos, datos.instagram_redsocial, datos.facebook_redsocial]
    if n==1:
        return datos.tiktok_redsocial
    if n==2:
        return datos.instagram_redsocial
    if n==3:
        return datos.facebook_redsocial
    if n==4:
        return datos.correo_contacto
    if n==5:
        return datos.correo_sugerencias_reclamos



#######Métodos de formateo
@register.filter(name="ejemploFiltro")
def ejemploFiltro(parametro):
	return f"el valor de parámetro es {parametro}"


@register.filter(name='numberFormat')
def numberFormat(numero):
    if numero == None:
        return 0
    else:
        return "{:,}".format(numero).replace(",",".")


@register.filter(name='invierteFecha')
def invierteFecha(fechaDateTime):
    fecha = fechaDateTime.strftime('%d/%m/%Y')
    return fecha


@register.filter(name='invierteFechaHora')
def invierteFechaHora(fechaDateTime):
    fecha = fechaDateTime.strftime('%d-%m-%Y %H:%M:%S')
    return fecha

 

####fecha###

def nombreDia(n):
    if n==0:
        return f"lunes"
    if n==1:
        return "Martes"
    if n==2:
        return "Miercoles"
    if n==3:
        return "Jueves"
    if n==4:
        return "Viernes"
    if n==5:
        return "Sabado"
    if n==6:
        return "Domingo"

def current_date_format(date):
    months = ("Enero", "Febrero", "Marzo", "Abri", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre")
    day = date.day  
    month = months[date.month - 1]
    year = date.year
    messsage = "{} de {} del {}".format(day, month, year)
    
    return messsage

### que dia es ###

@register.filter(name='queDiaes')
def queDiaes(fecha):
    numero = fecha.weekday()
    nombre_dia =  nombreDia(numero)
    fechaformateada = current_date_format(fecha)
    return f"{nombre_dia} {fechaformateada}"

@register.filter(name='conReserva')
def conReserva(id):
    
    return Reserva_activa.objects.filter(reserva_id__exact = id).exists()
        
    
    
    
@register.filter(name='conReservaActiva')
def conReservaActiva(id,fecha):
    return Reserva_activa.objects.filter(user_id__exact = id, fecha__contains = fecha).exists()

 
@register.filter(name='get_planes_choices')
def get_planes_choices(comunidad):
    planes = Planes.objects.filter(comunidad_id = comunidad)
    return planes

@register.filter(name='existenAlumnos')
def existenAlumnos(comunidad):    
    return Perfil.objects.filter(comunidad_id = comunidad).exists()

@register.filter(name='informacionPerfil')
def informacionPerfil(id):
    datos = Planes.objects.filter(id__exact = id).first()
    return datos.titulo

@register.filter(name='existePlanAsignado')
def existePlanAsignado(plan):    
    return Perfil.objects.filter(plan_id = plan).exists()

@register.filter(name='estadoReservaClase')
def estadoReservaClase(id):    
    dato = Reserva_estado.objects.get(id = id)
    return dato.estado
