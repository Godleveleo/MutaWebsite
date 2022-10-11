from django.contrib import admin
from myclasses.models import *
from utilidades.formularios import *


class BoxAdmin(admin.ModelAdmin):
    pass
admin.site.register(Box, BoxAdmin)

class ClasesAdmin(admin.ModelAdmin):
    pass

admin.site.register(Clases, ClasesAdmin)


class ReservaAdmin(admin.ModelAdmin):
    pass

admin.site.register(Reserva, ReservaAdmin)




class DisplicinaAdmin(admin.ModelAdmin):
    list_display = ('codigo','tipo','horario')
    icon_name = 'fitness_center'

admin.site.register(Disciplina, DisplicinaAdmin)

class PlanesAdmin(admin.ModelAdmin):
    list_display = ('Titulo','precio','TipoDisciplina','cantidadClases')
    search_fields= ('Titulo',)
    icon_name = 'format_list_numbered'               
admin.site.register(Planes, PlanesAdmin)


class EstudianteAdmin(admin.ModelAdmin):
    list_display = ('nombreCompleto',)
    search_fields= ('',)
    icon_name = 'portrait'
     

admin.site.register(UsersMetadata, EstudianteAdmin)

class IncripcionAdmin(admin.ModelAdmin):
    list_display = ('matricula', 'fecha')
    search_fields= ('matricula',)
    icon_name = 'playlist_add_check' 
admin.site.register(Matricula, IncripcionAdmin)


class PerfilAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombrePerfil', 'foto')
    search_fields= ('id',)
    icon_name = 'playlist_add_check' 

    def foto(self, obj):
        return format_html(f""" <a href="/media/{obj.imagenPerfil}" target="_blank">
            <img src="/media/{obj.imagenPerfil}" width="100" height="100" />
            </a> """)


admin.site.register(Perfil, PerfilAdmin)
