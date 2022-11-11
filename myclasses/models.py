# -*- encoding: utf-8 -*-
from django.utils.html import format_html
from django.db import models
# from autoslug import AutoSlugField
from django.contrib.auth.models import User
#signal
from django.db.models.signals import post_save, pre_save, pre_delete
from django.dispatch import receiver
##


#Establecimiento

class Box(models.Model):
    box = models.CharField(max_length=20, null=True,  verbose_name="Gimnasio")
    ubicacion = models.CharField(max_length=20, null=True, verbose_name="Ubicación")
    descripcion = models.CharField(max_length=400, null=True, verbose_name="Reseña")
    user_creador = models.CharField(max_length=40, null=True, verbose_name="creado")
    logo = models.ImageField(upload_to="logo", default= "logo/sinfoto.png" , verbose_name="logo")

    class Meta:
        verbose_name = "Gimnasio"
        verbose_name_plural = "Gimnasios" 

    def __str__(self) :
         txt = " {0}"
         return txt.format(self.box) 



    class Meta:
        verbose_name = "Disciplina"
        verbose_name_plural = "Disciplinas"

    def __str__(self) :
         txt = " Disciplina: {0} Horario: {1}"
         return txt.format( self.tipo, self.horario)


#extension de USER
class UsersMetadata(models.Model):
    id = models.AutoField(primary_key=True)    
    user = models.ForeignKey(User, models.DO_NOTHING, null= True)
    ced_identidad = models.CharField(max_length=9, verbose_name="Cedula de identidad")
    comunidad = models.ForeignKey(Box,max_length=100, null=True, blank=False, on_delete=models.DO_NOTHING, verbose_name="Comunidad")
    fechaNacimiento = models.DateField(verbose_name="Fecha de Nacimiento", null=True)
    sexos = [
        ('F', 'Femenino'),
        ('M' ,'Masculino'),
        ('N.N', 'Prefiero no Decirlo')
    ]
    sexo = models.CharField(max_length=30, choices=sexos, default='Prefiero no Decirlo')   
    

    class Meta:
        verbose_name = "User metadata"
        verbose_name_plural = "User metadata"    

    def nombreCompleto(self):
         txt = "{0}  {1}"
         return txt.format(self.user.first_name, self.user.last_name)
    nombreCompleto.short_description = 'Usuario'

    def __str__(self) :
         txt = " {0}"
         return txt.format(self.user.first_name, self.user.last_name)


    
class Planes(models.Model):    
    titulo = models.CharField(max_length=30, verbose_name="Nombre del plan")
    disciplina = models.CharField(max_length=40, verbose_name="Displinina")
    hora = [
        ('AM', 'Mañana'),
        ('PM' ,'Tarde'),
        ('AM/PM', 'AM/PM')
    ]       
    horario = models.CharField(max_length=13,  choices=hora, verbose_name="Horario del plan")  
    precio = models.PositiveIntegerField( null=False, blank=False, verbose_name="Precio del  plan")
    cantidad_clases =  models.PositiveSmallIntegerField(default=1, verbose_name="Clases por Semana")
    user_creador = models.CharField(max_length=40, null=True, verbose_name="creado")
    
    class Meta:
        verbose_name = "Planes"
        verbose_name_plural = "Planes"

    def price_display(self):
        return "{0:.3f}".format(self.precio / 100)
        


    def __str__(self) :
        txt = "Plan: {0} , Precio:$ {1} / {2} clases por semana"
        return txt.format(self.Titulo, self.precio, self.cantidadClases )

#clases
class Clases(models.Model):
    user_creador = models.CharField(max_length=40, null=True, verbose_name="creado")
    descripcion = models.CharField(max_length = 50, null=True)    
    modalidad = models.CharField(max_length=30,  null=True, verbose_name="Modalidad de clase")
    inicioClase = models.CharField( max_length=6, verbose_name="Inicio de clase")  
    terminoClase = models.CharField(max_length=6, verbose_name="Termino de clase")  
    duracion = models.PositiveIntegerField(default=1, null=False, blank=False, verbose_name="Duracion de Clase")
    cupo = models.PositiveIntegerField(default=1, null=False, blank=False, verbose_name="Nro. de cupos")
    
    class Meta:
        verbose_name = "Clases"
        verbose_name_plural = "Clases"

    def __str__(self) :
        txt = "Clase: {0} ,  {1} "
        return txt.format(self.Descripcion, self.modalidad)

 ##perfiles       
class Perfil(models.Model):
    nombre =models.ForeignKey(UsersMetadata,max_length=100, null=True, blank=False, on_delete=models.DO_NOTHING, verbose_name="Nombre")   
    # DisciplinaInscrita = models.ForeignKey(Disciplina, null=True, blank=False, on_delete=models.DO_NOTHING, verbose_name="Disciplina inscrita")
    plan = models.ForeignKey(Planes,max_length=20, null=True, blank=False, on_delete = models.DO_NOTHING, verbose_name="Plan Inscrito")     
    vigencia = models.BooleanField(default=True, verbose_name="Vigente")
    imagenPerfil = models.ImageField(upload_to="perfil", default= "perfil/sinfoto.png" , verbose_name="Imagen de Perfil")

    def __str__(self) :
        txt = "{0} {1}  "
        return txt.format( self.nombre.user.first_name , self.nombre.user.last_name)

    def nombrePerfil(self):
        txt = "{0} {1}"
        return txt.format(self.nombre.user.first_name, self.nombre.user.last_name)
    nombrePerfil.short_description = 'Nombre Completo'

    class Meta:
        verbose_name = "Perfiles"
        verbose_name_plural = "Perfiles"



# reservas

class Reserva_estado(models.Model):
    id = models.AutoField(primary_key=True)
    clase = models.ForeignKey(Clases,max_length=100, null=True, blank=False, on_delete=models.DO_NOTHING, verbose_name="Clase reservada")    
    comunidad = models.ForeignKey(Box,max_length=100, null=True, blank=False, on_delete=models.DO_NOTHING, verbose_name="Comunidad")    
    cupo = models.PositiveIntegerField( null=False, blank=False, verbose_name="Cupos Total")
    cupo_reservado = models.PositiveIntegerField(default=0, null=True, blank=False, verbose_name="Cupos Total")
    estado = models.BooleanField(default=True, verbose_name="Estado")
    barra_cupo = models.PositiveIntegerField(default=0,  blank=False, verbose_name="Cupos Total")
    user_creador = models.CharField(max_length=40, null=True, verbose_name="creado")
    Fecha = models.CharField(max_length = 20,null=True,verbose_name="fecha que se encuentra disponible la clase")
   
    

#matriculas
class Matricula(models.Model):
    matricula = models.CharField(max_length = 200, null=True, verbose_name="Alumno Matriculado")
    plan = models.CharField(max_length = 200, null=True, verbose_name="Disciplina")
    disInscrita = models.CharField(max_length = 200, null=True, verbose_name="Disciplina")
    vigencia = models.BooleanField(default=True, verbose_name="Estado")    
    fecha = models.DateTimeField(auto_now=True)

    
    class Meta:
        verbose_name = "Alumno matriculado"
        verbose_name_plural = "Alumnos matriculados"

    def __str__(self) :
        txt = "{0} /  Estado: {1} "
        if self.vigencia == 1:
            estadoEstdiante = "VIGENTE"
        else:
            estadoEstdiante = "EXPIRADO"

        return txt.format( self.matricula, estadoEstdiante)


class Reserva_activa(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.PositiveIntegerField( null=True, blank=False, verbose_name="Id del usuario que reserva")
    reserva_id = models.PositiveIntegerField( null=False, blank=False, verbose_name="Id del usuario que reserva")
    comunidad = models.PositiveIntegerField( null=False, blank=False, verbose_name="Id del usuario que reserva")
    fecha = models.CharField(max_length=20, verbose_name="fecha")

#signal        

@receiver(post_save, sender=Perfil)
def estudiando_new(sender, instance, **kwargs):
     if kwargs['created']:        
         Matricula.objects.create(matricula=f"{instance.nombre.user.first_name} {instance.nombre.user.last_name}" , disInscrita=f"{instance.DisciplinaInscrita.tipo}", plan=f"{instance.plan}")


        
       
        







