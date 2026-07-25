from django.db import models
from accounts.models import Department, User

class SemesterArchive(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='archives')
    academic_year = models.CharField(max_length=20)
    semester = models.IntegerField()
    total_projects = models.IntegerField(default=0)
    average_health_score = models.FloatField(default=0.0)
    archived_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    archived_at = models.DateTimeField(auto_now_add=True)
    summary_report_pdf = models.FileField(upload_to='archives/reports/', blank=True, null=True)

    class Meta:
        ordering = ['-archived_at']

    def __str__(self):
        return f"{self.department.code} Archive - {self.academic_year} (Sem {self.semester})"

class DepartmentAnalytics(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='analytics_snapshots')
    date_generated = models.DateField(auto_now_add=True)
    active_projects = models.IntegerField(default=0)
    completed_projects = models.IntegerField(default=0)
    high_risk_projects = models.IntegerField(default=0)
    total_students = models.IntegerField(default=0)
    total_faculty = models.IntegerField(default=0)
    avg_innovation_score = models.FloatField(default=0.0)

    class Meta:
        ordering = ['-date_generated']

    def __str__(self):
        return f"Analytics for {self.department.name} ({self.date_generated})"
