from django.contrib import admin
from .models import *
from import_export import resources
from import_export.admin import ImportExportModelAdmin
# Register your models here.

# Register your models here.
class onCallResource(resources.ModelResource):
    class meta:
        model=(Incidencia,IncideciaHijo)


@admin.register(Incidencia)
class IncidenciadProject(ImportExportModelAdmin, admin.ModelAdmin):
    resouce_class = onCallResource

    list_display = ('folio', )
    search_fields = ('folio',)

@admin.register(IncideciaHijo)
class IncideciaHijoProject(ImportExportModelAdmin, admin.ModelAdmin):
    resouce_class = onCallResource

    list_display = ('folio', )
    search_fields = ('folio',)


@admin.register(Elemento)
class ElementoProject(ImportExportModelAdmin, admin.ModelAdmin):
    resouce_class = onCallResource

    list_display = ('nombre', )
    search_fields = ('nombre',)