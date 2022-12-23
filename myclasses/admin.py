from django.contrib import admin
from myclasses.models import *
from utilidades.formularios import *



class KeywordsAdmin(admin.ModelAdmin):
    list_display = ('instagram_redsocial','tiktok_redsocial','facebook_redsocial', 'correo_contacto', 'correo_sugerencias_reclamos')
    icon_name = 'fitness_center'   
            

admin.site.register(Keywords, KeywordsAdmin)

class BoxAdmin(admin.ModelAdmin):
    list_display = ('box','ubicacion','descripcion')
    icon_name = 'fitness_center'   
            

admin.site.register(Box, BoxAdmin)


class ClasesAdmin(admin.ModelAdmin):
    list_display = ('descripcion','modalidad','inicioClase', 'terminoClase', 'duracion', 'cupo',)
    icon_name = 'fitness_center'

admin.site.register(Clases, ClasesAdmin)




class PlanesAdmin(admin.ModelAdmin):
    list_display = ('titulo','precio','cantidad_clases')
    search_fields= ('Titulo',)
    icon_name = 'format_list_numbered'

    

admin.site.register(Planes, PlanesAdmin)

    

class EstudianteAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombreCompleto',)
    search_fields= ('',)
    icon_name = 'portrait'
     

admin.site.register(UsersMetadata, EstudianteAdmin)

class IncripcionAdmin(admin.ModelAdmin):
    list_display = ('matricula', 'fecha', 'vigencia')
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




admin.site.site_header = 'ClassBox'
admin.site.index_title = 'Panel de control de ClassBox'
admin.site.site_title = 'ClassBox'




# def queryset(self, request):
       
#         qs = super(ThisAdmin, self).queryset(request)
#         if request.user.is_superuser:
#             return qs
#         return qs.filter(owner=request.user)