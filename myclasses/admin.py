from django.contrib import admin
from myclasses.models import *

class DisplicinaAdmin(admin.ModelAdmin):
    list_display = ('codigo','tipo', 'horario')

admin.site.register(Disciplina, DisplicinaAdmin)

class PlanesAdmin(admin.ModelAdmin):
    list_display = ('Titulo','precio','cantidadClases')
    search_fields= ('Titulo',)

admin.site.register(Planes, PlanesAdmin)

class EstudianteAdmin(admin.ModelAdmin):
    list_display = ('ced_identidad','nombres','apellidoPaterno', 'apellidoMaterno','tipo', 'plan')
    search_fields= ('ced_identidad',)

admin.site.register(Estudiante, EstudianteAdmin)

class IncripcionAdmin(admin.ModelAdmin):
    list_display = ('id','alumno','fechaIncripcion')
    search_fields= ('alumno',)

admin.site.register(Incripciones, IncripcionAdmin)
