from email.policy import default
from django.db import models
from autoslug import AutoSlugField
from django.contrib.auth.models import User
#signal
from django.db.models.signals import post_save, pre_save, pre_delete
from django.dispatch import receiver

from django.utils.html import format_html
from myclasses import dreamhost


class Disciplina(models.Model):
    codigo = models.CharField(max_length=3, primary_key=True)
    tipo = models.CharField(max_length=50, verbose_name="Disciplina")
    hora = [
        ('AM', 'Mañana'),
        ('PM' ,'Tarde'),
        ('AM/PM', 'AM/PM')
    ]    
    horario = models.CharField(max_length=13,  choices=hora, verbose_name="Horario de clases")

    class Meta:
        verbose_name = "Disciplina"
        verbose_name_plural = "Disciplinas"

    def __str__(self) :
        txt = "Codigo: {0} Disciplina: {1} Horario: {2}"
        return txt.format(self.codigo, self.tipo, self.horario)
    
class Planes(models.Model):    
    Titulo = models.CharField(max_length=30, verbose_name="Nombre del plan")    
    TipoDisciplina = models.ForeignKey(Disciplina,max_length=20, null=True, blank=False, on_delete = models.DO_NOTHING, verbose_name="Asociado")
    precio = models.PositiveIntegerField(default=0, null=False, blank=False, verbose_name="Precio del  plan")
    cantidadClases =  models.PositiveSmallIntegerField(default=1, verbose_name="Clases por Semana")

    class Meta:
        verbose_name = "Planes"
        verbose_name_plural = "Planes"

    def price_display(self):
        return "{0:.3f}".format(self.precio / 100)
        


    def __str__(self) :
        txt = "Plan: {0} , Precio:$ {1} / {2} clases por semana"
        return txt.format(self.Titulo, self.precio, self.cantidadClases )

class UsersMetadata(models.Model):
    user = models.ForeignKey(User, models.DO_NOTHING, null= True)
    ced_identidad = models.CharField(max_length=9, primary_key=True, verbose_name="Cedula de identidad")
    # apellidoPaterno = models.CharField(max_length=35, verbose_name="Apellido Paterno")
    # apellidoMaterno = models.CharField(max_length=35, verbose_name="Apellido Materno")
    # nombres = models.CharField(max_length=35, verbose_name="Nombres")
    fechaNacimiento = models.DateField(verbose_name="Fecha de Nacimiento")
    sexos = [
        ('F', 'Femenino'),
        ('M' ,'Masculino'),
        ('N.N', 'Prefiero no Decirlo')
    ]
    sexo = models.CharField(max_length=30, choices=sexos, default='Prefiero no Decirlo')
    tipo = models.ForeignKey(Disciplina, null=False, blank=False, on_delete=models.CASCADE, verbose_name="Disciplina inscrita")
    plan = models.ForeignKey(Planes,max_length=20, null=False, blank=False, on_delete = models.DO_NOTHING, verbose_name="Plan Inscrito") 
    # correo = models.EmailField(blank=False, verbose_name="Correo electronico")
    vigencia = models.BooleanField(default=True, verbose_name="Vigente")
    imagenPerfil = models.ImageField(upload_to="Foto_Perfil",blank=True, null=True, default= "default.png" , verbose_name="Imagen de Perfil")

    class Meta:
        verbose_name = "User metadata"
        verbose_name_plural = "User metadata"

    def nombreCompleto(self):
         txt = "{0}  {1}"
         return txt.format(self.user.first_name, self.user.last_name)

    nombreCompleto.short_description = 'Usuario'

    def __str__(self) :
        txt = "{0} / {1} / Estado: {2} "
        if self.vigencia == 1:
            estadoEstdiante = "VIGENTE"
        else:
            estadoEstdiante = "EXPIRADO"

        return txt.format( self.tipo, self.plan, estadoEstdiante)



class Incripciones(models.Model):
    matricula = models.CharField(max_length = 200, null=True)
    fecha = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Alumno matriculado"
        verbose_name_plural = "Alumnos matriculados"


#signal        

@receiver(post_save, sender=UsersMetadata)
def estudiando_new(sender, instance, **kwargs):
    if kwargs['created']:
        Incripciones.objects.create(matricula=f"{instance.user.first_name} {instance.user.last_name} {instance.plan} | Disciplina: {instance.tipo.tipo}")


def foto_perfil(obj):
    if dreamhost.existeArchivo('Foto_Perfil', obj.imagenPerfil)==False:
        dreamhost.moverArchivoProducto(obj.imagenPerfil, obj.ced_identidad)

    return format_html(f""" <a href="/assets/upload/Foto_Perfil/{obj.imagenPerfil}" target="_blank">
		<img src="/assets/upload/Foto_Perfil/{obj.imagenPerfil}" width="100" height="100" />
		</a> """)

foto_perfil.short_description = 'Foto de Perfil'






