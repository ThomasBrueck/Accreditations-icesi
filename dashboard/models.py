from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
#import from init.models import UserModel
from init.models import UserModel, RoleModel
from django.utils import timezone 

class PermissionModel(models.Model):
    name = models.CharField(max_length=50)  # Ej: "read_report", "write_template"
    description = models.CharField(max_length=255, blank=True)  # Descripción opcional
    roles = models.ManyToManyField(RoleModel, blank=True, related_name="permissions")  # Relación inversa

    def __str__(self):
        return self.name

class ReportModel(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]

    name = models.CharField(max_length=150)
    description = models.TextField(max_length=300)
    image = models.ImageField(upload_to='reports/', blank=True, null=True)
    end_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    created_by = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='reports')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} {self.created_by.username}"

class FactorModel(models.Model):
    STATUS_CHOICES = [('active', 'Active'), ('inactive', 'Inactive')]
    MAX_CONTENT = 5000

    name = models.CharField(max_length=100)
    content = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    google_doc_url = models.URLField(max_length=200, blank=True, null=True)
    progress = models.IntegerField(default=0)
    last_edited_by = models.ForeignKey(UserModel, on_delete=models.SET_NULL, null=True)
    report = models.ForeignKey(ReportModel, on_delete=models.CASCADE, related_name='factors')
    updated_at = models.DateTimeField(auto_now=True)
    end_date = models.DateField(null=True, blank=True)

    @property
    def progress_percentage(self):
        if not self.pk:
            return 0
        
        total_characteristics = self.characteristics.count()
        if total_characteristics == 0:
            return 0
        completed_characteristics = self.characteristics.filter(state__name="Completed").count()
        return int((completed_characteristics / total_characteristics) * 100)

    def save(self, *args, **kwargs):
        if self.pk:
            self.progress = self.progress_percentage
        else:
            self.progress = 0

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} - {self.report.name}"


# New QuestionModel
class QuestionModel(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('answered', 'Answered'),
    ]
    factor = models.ForeignKey(FactorModel, on_delete=models.CASCADE, related_name='questions')
    owner = models.ForeignKey(UserModel, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)  # This will be the question
    answer = models.TextField(blank=True)  # New field for the answer
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    answered_by = models.ForeignKey(UserModel, on_delete=models.SET_NULL, null=True, blank=True, related_name='answered_questions')
    answered_at = models.DateTimeField(null=True, blank=True)
    question_edited = models.BooleanField(default=False)  # New field to track question edits
    answer_edited = models.BooleanField(default=False)  # New field to track answer edits

    def __str__(self):
        return self.title

class CommentsModel(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('not_approved', 'Not Approved'),
    ]

    factor = models.ForeignKey(FactorModel, on_delete=models.CASCADE, related_name='comments')
    owner = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    justification = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)  # Temporalmente sin auto_now_add
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class AnswerModel(models.Model):
    owner = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    content = models.TextField(max_length=500)
    updated_at = models.DateTimeField(auto_now=True)
    question = models.ForeignKey(QuestionModel, on_delete=models.CASCADE, null=True, blank=True, related_name='answers')
    comment = models.ForeignKey(CommentsModel, on_delete=models.CASCADE, null=True, blank=True, related_name='answers')

    def __str__(self):
        return f"Answer by {self.owner.username}"


class States(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class GlobalStrengths(models.Model):
    name = models.CharField(max_length=200, unique=True)
    created_by = models.ForeignKey(UserModel, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class GlobalAspects(models.Model):
    name = models.CharField(max_length=200, unique=True)
    created_by = models.ForeignKey(UserModel, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class CharacteristicModel(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    factors = models.ManyToManyField(FactorModel, related_name='characteristics')
    created_by = models.ForeignKey(UserModel, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    state = models.ForeignKey(States, on_delete=models.SET_NULL, null=True, default=None)  # Cambiado a ForeignKey

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.state:  # Si es la primera vez que se guarda
            self.state, created = States.objects.get_or_create(name="In Progress")
        super().save(*args, **kwargs)

    @property
    def has_strengths_and_aspects(self):
        return self.strengths.exists() and self.aspects.exists()

class CharacteristicStrengths(models.Model):
    characteristic = models.ForeignKey(CharacteristicModel, on_delete=models.CASCADE, related_name='strengths')
    global_strength = models.ForeignKey(GlobalStrengths, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('characteristic', 'global_strength')

class CharacteristicAspects(models.Model):
    characteristic = models.ForeignKey(CharacteristicModel, on_delete=models.CASCADE, related_name='aspects')
    global_aspect = models.ForeignKey(GlobalAspects, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('characteristic', 'global_aspect')

# ... (otros modelos)
    
class NotificationModel(models.Model):
    title = models.CharField(max_length=100)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name="notifications")
    created_by = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name="created_notifications")
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title} - {self.created_by}"
    
class TaskModel(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
    ]

    title = models.CharField(max_length=100)
    due_date = models.DateField()
    assignee = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='tasks_assigned')
    created_by = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='tasks_created')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - Assigned to {self.assignee.username}"
    
class NotificationLog(models.Model):
    recipient = models.EmailField(max_length=255, verbose_name="Destinatario")
    sent_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Envío")
    created_by = models.ForeignKey(UserModel, on_delete=models.CASCADE, verbose_name="Enviado por")  # Cambiado a UserModel

    def __str__(self):
        return f"Notificación a {self.recipient} - {self.sent_at}"

    class Meta:
        verbose_name = "Registro de Notificación"
        verbose_name_plural = "Registros de Notificaciones"

class AccreditationProcess(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('planning', 'Planning'),
        ('analysis', 'Analysis'),
        ('evidence', 'Evidence'),
        ('report', 'Report'),
        ('consolidation', 'Consolidation'),
        ('submission', 'Submission'),
        ('completed', 'Completed'),
    ]

    name = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    start_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='text_board_accreditation_processes'
    )

    def __str__(self):
        return self.name