from django.contrib import admin
from myclasses.models import *



class DisplicinaAdmin(admin.ModelAdmin):
    list_display = ('tipo','codigo','horario')
    icon_name = 'fitness_center'

admin.site.register(Disciplina, DisplicinaAdmin)

class PlanesAdmin(admin.ModelAdmin):
    list_display = ('Titulo','precio','TipoDisciplina','cantidadClases')
    search_fields= ('Titulo',)
    icon_name = 'format_list_numbered'               

admin.site.register(Planes, PlanesAdmin)

class EstudianteAdmin(admin.ModelAdmin):
    list_display = ('ced_identidad','nombres','apellidoPaterno', 'apellidoMaterno','tipo', 'plan')
    search_fields= ('ced_identidad',)
    icon_name = 'portrait' 

admin.site.register(Estudiante, EstudianteAdmin)

class IncripcionAdmin(admin.ModelAdmin):
    list_display = ('id','alumno','fechaIncripcion')
    search_fields= ('alumno',)
    icon_name = 'playlist_add_check' 
admin.site.register(Incripciones, IncripcionAdmin)


