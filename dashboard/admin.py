from django.contrib import admin
from .models import PermissionModel, ReportModel # Añadimos PermissionModel

# Register your models here

class PermissionAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "get_roles")  # Mostramos nombre, descripción y roles

    def get_roles(self, obj):
        # Obtenemos los nombres de los roles asociados al permiso
        return ", ".join([role.name for role in obj.roles.all()])
    
    get_roles.short_description = "Roles"  # Título de la columna

class ReportAdmin(admin.ModelAdmin):
    list_display = ("name", "get_created_by", )

    def get_created_by(self, obj):
        return obj.created_by.username
    
    get_created_by.short_description = 'created by'

# Registramos PermissionModel
admin.site.register(PermissionModel, PermissionAdmin)
admin.site.register(ReportModel, ReportAdmin)
