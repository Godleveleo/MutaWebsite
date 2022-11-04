import string
import random
from django.utils.text import slugify
from myclasses.models import *
from django.utils.html import format_html
from utilidades import dreamhost
from functools import wraps
from django.contrib.auth import authenticate, login, logout
from django.http import Http404, HttpResponseRedirect
from django.contrib import messages


def logueado():
    def _activo_required(func):
        @wraps(func)
        def _decorator(request, *args, **kwargs):
            if not request.user.is_authenticated:
                messages.add_message(request, messages.WARNING, 'Debes estar logueado para visualizar este contenido.')
                return HttpResponseRedirect('/acceso/login')
            else:
                return func(request, *args, **kwargs)
        return _decorator
    return _activo_required

def foto_perfil(obj):
    if dreamhost.existeArchivo('perfil', obj.imagenPerfil) == False:
        dreamhost.moverArchivoProducto(obj.imagenPerfil, obj.id)

    return format_html(f""" <a href="/assets/upload/{obj.imagenPerfil}" target="_blank">
		<img src="/assets/upload/{obj.imagenPerfil}" width="100" height="100" />
		</a> """)

foto_perfil.short_description = 'Foto de Perfil'



def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def unique_slug_generator(instance, new_slug=None):
    """
    Este es para un proyecto de Django y se asume que la instancia
    tiene un modelo con un campo de slug (Slugfield) y un titulo de CharField
    """
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instance.title)

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(slug=slug).exists()
    if qs_exists:
        new_slug = "{slug}-{randstr}".format(
            slug=slug,
            randstr=random_string_generator(size=4)
        )
        return unique_slug_generator(instance, new_slug=new_slug)
    return slug


def get_clases_choices():
	return [
	(value.pk, value.descripcion,) for value in Clases.objects.all()
	]
def get_box_choices():
	return [
	(value.pk, value.box,) for value in Box.objects.all()
	]

def porcentaje(cupototal, cupoReservado):

    resultado = int(cupoReservado / cupototal * 100)

    return resultado

def get_clases_cuportotal(clase):
    
	return [
	(value.cupo) for value in Clases.objects.filter(id__exact = clase)
	]

def is_member(user):
    return user.groups.filter(name='manager').exists()

def is_member_alumno(user):
    return user.groups.filter(name='alumnos').exists()

def reserva_active(userid):
    return Reserva_activa.objects.filter(user_id__exact = userid).exists()

def get_reservaid(userid):
    id_reserva = None
    if not Reserva_activa.objects.filter(user_id__exact = userid).exists():
        id_reserva = 0
    else:
        dato = Reserva_activa.objects.filter(user_id__exact = userid).first()
        id_reserva = dato.reserva_id     

    return id_reserva
