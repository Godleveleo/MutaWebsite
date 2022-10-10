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
    list_display = ('nombreCompleto','ced_identidad','tipo', 'plan', foto_perfil)
    search_fields= ('ced_identidad',)
    icon_name = 'portrait'
     

admin.site.register(UsersMetadata, EstudianteAdmin)

class IncripcionAdmin(admin.ModelAdmin):
    list_display = ('matricula', 'fecha')
    search_fields= ('matricula',)
    icon_name = 'playlist_add_check' 
admin.site.register(Incripciones, IncripcionAdmin)


