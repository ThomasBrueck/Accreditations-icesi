from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.db import connection
from django.apps import apps

@receiver(post_migrate)
def create_default_roles(sender, **kwargs):
    if sender.name == 'init':
        RoleModel = apps.get_model('init', 'RoleModel')
        
        if RoleModel._meta.db_table in connection.introspection.table_names():
            roles = ["acadi", "program director", "common"]
            for role in roles:
                RoleModel.objects.get_or_create(name=role)
