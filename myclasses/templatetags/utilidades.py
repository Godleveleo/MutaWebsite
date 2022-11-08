from django import template
from myclasses.models import *


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
    datos=Metadata.objects.get()
    lista=[datos.keyword, datos.description, datos.correo, datos.telefono, datos.titulo]
    if n==1:
        return datos.keyword
    if n==2:
        return datos.description
    if n==3:
        return datos.correo
    if n==4:
        return datos.telefono
    if n==5:
        return datos.titulo



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