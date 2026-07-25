import json
from django.db import models
from django.utils import timezone
from accounts.models import User
from projects.models import Project

class KnowledgeVault(models.Model):
    class Category(models.TextChoices):
        LESSON_LEARNED = 'LESSON_LEARNED', 'Lessons Learned'
        BEST_PRACTICE = 'BEST_PRACTICE', 'Best Practices'
        FUTURE_IMPROVEMENT = 'FUTURE_IMPROVEMENT', 'Future Improvements'
        ARCHITECTURE = 'ARCHITECTURE', 'Architecture Pattern'

    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True, blank=True, related_name='vault_entries')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    category = models.CharField(max_length=30, choices=Category.choices, default=Category.LESSON_LEARNED)
    content = models.TextField(help_text="Detailed knowledge article, solution, or insight")
    tags = models.CharField(max_length=255, blank=True, help_text="Comma-separated tags (e.g. Django, Security, Performance)")
    is_public = models.BooleanField(default=True, help_text="Available across entire academic department")
    upvotes = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"[{self.get_category_display()}] {self.title}"

class ProjectSnapshot(models.Model):
    """
    Core Model backing Replay Mode:
    Captures complete point-in-time evolution metrics of a project.
    """
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='snapshots')
    version_number = models.IntegerField()
    snapshot_timestamp = models.DateTimeField(default=timezone.now)
    snapshot_hash = models.CharField(max_length=64, blank=True)
    health_score = models.FloatField()
    innovation_score = models.FloatField()
    total_work_logs = models.IntegerField(default=0)
    total_bugs_resolved = models.IntegerField(default=0)
    summary_note = models.TextField(blank=True, default='')
    snapshot_json = models.TextField(default='{}', help_text="JSON payload of tasks, milestones, and status at snapshot moment")

    class Meta:
        ordering = ['version_number']
        unique_together = ('project', 'version_number')

    def get_snapshot_data(self):
        try:
            return json.loads(self.snapshot_json)
        except Exception:
            return {}

    def __str__(self):
        return f"{self.project.title} - Snapshot v{self.version_number} ({self.snapshot_timestamp.strftime('%Y-%m-%d')})"

class RiskAssessment(models.Model):
    """
    Core Model backing Risk Prediction Engine.
    """
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='risk_assessments')
    risk_score = models.FloatField(help_text="0-100 where higher means elevated delay risk")
    risk_category = models.CharField(max_length=20, choices=Project.RiskLevel.choices, default=Project.RiskLevel.LOW)
    predicted_delay_days = models.IntegerField(default=0)
    risk_factors_json = models.TextField(default='[]', help_text="JSON array of active risk flags")
    recommendations_json = models.TextField(default='[]', help_text="JSON array of corrective steps for faculty & students")
    assessed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-assessed_at']

    def get_factors(self):
        try:
            return json.loads(self.risk_factors_json)
        except Exception:
            return []

    def get_recommendations(self):
        try:
            return json.loads(self.recommendations_json)
        except Exception:
            return []

    def __str__(self):
        return f"{self.project.title} - Risk: {self.risk_category} ({self.risk_score}%)"

class ContributionScore(models.Model):
    """
    Core Model backing Student Contribution Analyzer.
    """
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='contribution_scores')
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='contribution_records')
    total_hours_logged = models.FloatField(default=0.0)
    work_logs_count = models.IntegerField(default=0)
    tasks_completed = models.IntegerField(default=0)
    bugs_resolved = models.IntegerField(default=0)
    calculated_percentage = models.FloatField(default=0.0, help_text="Contribution share percentage")
    grade_weight = models.FloatField(default=100.0, help_text="Relative mark multiplier")
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('project', 'student')

    def __str__(self):
        return f"{self.student.get_full_name() or self.student.username} ({self.calculated_percentage}%) in {self.project.title}"
