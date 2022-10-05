from django.db import models

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
    horario =  models.CharField(max_length=30, verbose_name="Inicio de clases")
    TipoDisciplina = models.ForeignKey(Disciplina,max_length=20, null=False, blank=False, on_delete = models.DO_NOTHING, verbose_name=" Tipo Disciplina")
    precio = models.CharField(max_length=8, null=False, blank=False, verbose_name="Precio del  plan")
    cantidadClases =  models.PositiveSmallIntegerField(default=1, verbose_name="Clases por Semana")

    class Meta:
        verbose_name = "Planes"
        verbose_name_plural = "Planes"

    def __str__(self) :
        txt = "Plan: {0} , Precio:$ {1} / {2} clases por semana"
        return txt.format(self.Titulo, self.precio, self.cantidadClases )

class Estudiante(models.Model):
    ced_identidad = models.CharField(max_length=9, primary_key=True, verbose_name="Cedula de identidad")
    apellidoPaterno = models.CharField(max_length=35, verbose_name="Apellido Paterno")
    apellidoMaterno = models.CharField(max_length=35, verbose_name="Apellido Materno")
    nombres = models.CharField(max_length=35, verbose_name="Nombres")
    fechaNacimiento = models.DateField(verbose_name="Fecha de Nacimiento")
    sexos = [
        ('F', 'Femenino'),
        ('M' ,'Masculino'),
        ('N.N', 'Prefiero no Decirlo')
    ]
    sexo = models.CharField(max_length=30, choices=sexos, default='Prefiero no Decirlo')
    tipo = models.ForeignKey(Disciplina, null=False, blank=False, on_delete=models.CASCADE, verbose_name="Disciplina inscrita")
    plan = models.ForeignKey(Planes,max_length=20, null=False, blank=False, on_delete = models.DO_NOTHING, verbose_name="Plan Inscrito") 
    correo = models.EmailField(blank=False, verbose_name="Correo electronico")
    vigencia = models.BooleanField(default=True, verbose_name="Estado del alumno")
    imagenPerfil = models.ImageField(upload_to="Foto_Perfil", null=True, verbose_name="Imagen de Perfil")

    

    def nombreCompleto(self):
        txt = "{0} {1}, {2}"
        return txt.format(self.nombres, self.apellidoPaterno, self.apellidoMaterno)

    def __str__(self) :
        txt = "{0} / {1} / {2} / Estado: {3} "
        if self.vigencia:
            estadoEstdiante = "VIGENTE"
        else:
            estadoEstdiante = "EXPERIDO"

        return txt.format(self.nombreCompleto(), self.tipo, self.plan, estadoEstdiante)


class Incripciones(models.Model):
    id = models.AutoField(primary_key=True)
    alumno = models.ForeignKey(Estudiante, null=False, blank=False, on_delete=models.CASCADE)
    fechaIncripcion = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Inscripcion"
        verbose_name_plural = "Inscripciones"

    def __str__(self) :
        txt = "{0} / {1}  "
        return txt.format(self.alumno, self.fechaIncripcion)


