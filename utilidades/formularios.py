import string
import random
from django.utils.text import slugify
from myclasses.models import *
from django.utils.html import format_html
from utilidades import dreamhost

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