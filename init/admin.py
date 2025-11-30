from django.contrib import admin
from .models import UserModel, VerificationCodeModel, RoleModel

# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", )

class VerificationCodeAdmin(admin.ModelAdmin):
    list_display = ("get_username", "get_email",)

    def get_username(self, obj):
        return obj.user.username
    
    def get_email(self, obj):
        return obj.user.email
    
    get_username.short_description = "username"
    get_email.short_description = "email"

class RoleAdmin(admin.ModelAdmin):
    list_display = ("name", "get_permissions")  # Mostramos nombre y permisos

    def get_permissions(self, obj):
        # Obtenemos los nombres de los permisos asociados al rol
        return ", ".join([perm.name for perm in obj.permissions.all()])
    
    get_permissions.short_description = "Permisos"  # Título de la columna

admin.site.register(UserModel, UserAdmin)
admin.site.register(VerificationCodeModel, VerificationCodeAdmin)
admin.site.register(RoleModel, RoleAdmin)  