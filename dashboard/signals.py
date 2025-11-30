from django.db.models.signals import post_migrate, post_save
from django.dispatch import receiver
from django.db import connection
from django.apps import apps
from .models import ReportModel, NotificationModel, UserModel

@receiver(post_migrate)
def setup_permissions(sender, **kwargs):
    if sender.name == 'dashboard':
        # Obtener modelos dinámicamente
        PermissionModel = apps.get_model('dashboard', 'PermissionModel')
        RoleModel = apps.get_model('init', 'RoleModel')

        # Verificar que ambas tablas existan
        tables = connection.introspection.table_names()
        if (PermissionModel._meta.db_table in tables and 
            RoleModel._meta.db_table in tables):
            # Crear permisos locales
            permissions = [
                {"name": "read_report", "description": "Puede leer informes"},
                {"name": "write_report", "description": "Puede escribir informes"},
                {"name": "update_report", "description": "Puede actualizar informes"},
                {"name": "read_template", "description": "Puede leer plantillas"},
                {"name": "write_template", "description": "Puede escribir plantillas"},
                {"name": "update_template", "description": "Puede actualizar plantillas"},
                {"name": "read_comment", "description": "Puede leer comentarios"},
                {"name": "write_comment", "description": "Puede escribir comentarios"},
                {"name": "update_comment", "description": "Puede actualizar comentarios"},
                {"name": "manage_characteristics", "description": "Puede gestionar características"},
            ]
            for perm in permissions:
                PermissionModel.objects.get_or_create(name=perm["name"], defaults={"description": perm["description"]})

            # Asignar permisos a los roles
            role_permissions = {
                'acadi': [
                    'read_report', 'write_report', 'update_report',
                    'read_template', 'write_template', 'update_template',
                    'read_comment', 'write_comment', 'update_comment',
                    'manage_characteristics'
                ],
                'program director': [
                    'read_report', 'write_report',
                    'read_template', 'write_template',
                    'read_comment', 'write_comment',
                    'manage_characteristics'
                ],
                'common': [
                    'read_report',
                    'read_template',
                    'read_comment'
                ]
            }

            for role_name, perm_names in role_permissions.items():
                role, created = RoleModel.objects.get_or_create(name=role_name)
                perms_to_assign = PermissionModel.objects.filter(name__in=perm_names)
                for perm in perms_to_assign:
                    perm.roles.add(role)

@receiver(post_save, sender=ReportModel)
def create_notification_for_admins(sender, instance, created, **kwargs):
    if created:
        for user in UserModel.objects.filter(role__name__in=['program director', 'acadi', 'common']):
            NotificationModel.objects.create(
                title=f"Report created: {instance.name}",
                user=user,
                created_by=instance.created_by
            )