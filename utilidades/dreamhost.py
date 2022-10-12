import os
import shutil
from myclasses.models import *
from django.conf import settings
from pathlib import Path
from datetime import datetime, date, timedelta

RUTA = settings.RUTA
RUTA2 = settings.RUTA2


def moverArchivoProducto(file, id):
	if existeArchivoMedia(file)==True:        
		fecha = datetime.now()                
		nombre = f"{datetime.timestamp(fecha)}{os.path.splitext(str(file))[1]}"
		shutil.move(f'MutaWebsite/{file}', f'assets/upload/{nombre}')
		Perfil.objects.filter(pk=id).update(imagenPerfil=nombre)

        



# def moverArchivoProducto3(file, id):
#     #if existeArchivoMedia(file)==True:
#     fecha = datetime.now()
#     nombre = f"{datetime.timestamp(fecha)}{os.path.splitext(str(file))[1]}"
#     shutil.move(f'{RUTA}myclasses/media/Foto_Perfil/{file}', f'{RUTA2}assets/upload/Foto_Perfil/{nombre}')
#     UsersMetadata.objects.filter(pk=id).update(foto=nombre)


# def moverArchivoProducto2(file):
#     shutil.move(f'{RUTA}myclasses/media/Foto_Perfil/{file}', f'{RUTA2}assets/upload/Foto_Perfil/{file}')


def existeArchivo(carpeta, archivo):
     try:
         ruta=f"{RUTA}MutaWebsite/assets/upload/{carpeta}/{archivo}"
         fileObj = Path(ruta)
         return fileObj.is_file()
     except Exception as e:
         return False


def existeArchivoMedia(archivo):
    try:
        ruta=f"{RUTA}MutaWebsite/{archivo}"
        fileObj = Path(ruta)
        return fileObj.is_file()
    except Exception as e:
          return False