from django.db import models
from django.contrib.auth.models import AbstractUser

class Department(models.Model):
    name = models.CharField(max_length=150, unique=True)
    code = models.CharField(max_length=20, unique=True)
    description = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.code})"

    class Meta:
        ordering = ['name']

class User(AbstractUser):
    class Role(models.TextChoices):
        STUDENT = 'STUDENT', 'Student'
        FACULTY = 'FACULTY', 'Faculty Guide'
        HOD = 'HOD', 'Head of Department'
        ADMIN = 'ADMIN', 'System Administrator'

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.STUDENT,
    )
    department = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='users'
    )
    roll_number = models.CharField(max_length=50, blank=True, null=True, unique=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    designation = models.CharField(max_length=100, blank=True, null=True)

    @property
    def is_student(self):
        return self.role == self.Role.STUDENT

    @property
    def is_faculty(self):
        return self.role == self.Role.FACULTY

    @property
    def is_hod(self):
        return self.role == self.Role.HOD

    @property
    def is_admin_role(self):
        return self.role == self.Role.ADMIN or self.is_superuser

    def get_dashboard_url(self):
        if self.is_student:
            return 'core:student_dashboard'
        elif self.is_faculty:
            return 'core:faculty_dashboard'
        elif self.is_hod:
            return 'core:hod_dashboard'
        elif self.is_admin_role:
            return 'core:admin_dashboard'
        return 'core:landing'

    def __str__(self):
        full_name = self.get_full_name()
        display = full_name if full_name else self.username
        return f"{display} [{self.get_role_display()}]"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True, default='')
    skills = models.CharField(max_length=255, blank=True, help_text='Comma-separated skills (e.g. Python, Django, React)')
    github_url = models.URLField(blank=True, null=True)
    linkedin_url = models.URLField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Profile of {self.user.username}"
