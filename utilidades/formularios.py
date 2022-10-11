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