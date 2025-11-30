from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class RoleModel(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name}"

class UserModel(AbstractUser):
    email = models.EmailField(unique=True)
    is_verified_acadi = models.BooleanField(default=False)
    is_verified_code = models.BooleanField(default=False)
    role = models.ForeignKey(RoleModel, on_delete=models.CASCADE, null=True, related_name="users")
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    # Por defecto el AbstractUser usa el username como identificador para la gestion de usuarios, pero 
    # a nostros nos interesa validar todo con el email y que el username solo sea una informacion a mostrar
    # en la pagina. Entonces el campo 'username' apunta al email, pero guarda el username del usuario
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return f"{self.username} {self.email}"
    
class VerificationCodeModel(models.Model):
    user = models.OneToOneField(UserModel, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    
    def __str__(self):
        return f"{self.user.email}"