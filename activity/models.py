from django.db import models
from django.utils import timezone
from accounts.models import User
from projects.models import Project, Milestone

class WorkLog(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='work_logs')
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='work_logs')
    milestone = models.ForeignKey(Milestone, on_delete=models.SET_NULL, null=True, blank=True, related_name='work_logs')
    title = models.CharField(max_length=200)
    description = models.TextField()
    hours_spent = models.DecimalField(max_digits=5, decimal_places=1, default=1.0)
    date_logged = models.DateField(default=timezone.now)
    
    # Upload attachments & source proof
    file_attachment = models.FileField(upload_to='work_logs/files/', blank=True, null=True)
    screenshot = models.ImageField(upload_to='work_logs/screenshots/', blank=True, null=True)
    code_snippet = models.TextField(blank=True, default='', help_text='Relevant code snippets or changes')
    commit_hash = models.CharField(max_length=40, blank=True, default='', help_text='Git commit SHA')

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_logged', '-created_at']

    def __str__(self):
        return f"{self.student.username} - {self.title} ({self.date_logged})"

class DecisionLog(models.Model):
    class Status(models.TextChoices):
        PROPOSED = 'PROPOSED', 'Proposed'
        ACCEPTED = 'ACCEPTED', 'Accepted & Architectural Standard'
        SUPERSEDED = 'SUPERSEDED', 'Superseded'
        REJECTED = 'REJECTED', 'Rejected'

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='decision_logs')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    context = models.TextField(help_text="What problem or architectural scenario required this decision?")
    decision_taken = models.TextField(help_text="What decision was made?")
    consequences = models.TextField(help_text="Pros, cons, and operational impacts")
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ACCEPTED)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"ADR-{self.id}: {self.title} [{self.get_status_display()}]"

class Task(models.Model):
    class Priority(models.TextChoices):
        LOW = 'LOW', 'Low'
        MEDIUM = 'MEDIUM', 'Medium'
        HIGH = 'HIGH', 'High'
        URGENT = 'URGENT', 'Urgent'

    class Status(models.TextChoices):
        TODO = 'TODO', 'To Do'
        IN_PROGRESS = 'IN_PROGRESS', 'In Progress'
        CODE_REVIEW = 'CODE_REVIEW', 'Code Review'
        DONE = 'DONE', 'Completed'

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_tasks')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_tasks')
    milestone = models.ForeignKey(Milestone, on_delete=models.SET_NULL, null=True, blank=True, related_name='tasks')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, default='')
    priority = models.CharField(max_length=20, choices=Priority.choices, default=Priority.MEDIUM)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.TODO)
    due_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['priority', 'due_date']

    def __str__(self):
        return f"[{self.get_status_display()}] {self.title}"

class BugReport(models.Model):
    class Severity(models.TextChoices):
        LOW = 'LOW', 'Low'
        MEDIUM = 'MEDIUM', 'Medium'
        HIGH = 'HIGH', 'High'
        CRITICAL = 'CRITICAL', 'Critical Blocking'

    class Status(models.TextChoices):
        OPEN = 'OPEN', 'Open'
        IN_TRIAGE = 'IN_TRIAGE', 'In Triage'
        RESOLVED = 'RESOLVED', 'Resolved'
        CLOSED = 'CLOSED', 'Closed'

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='bugs')
    reported_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reported_bugs')
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_bugs')
    title = models.CharField(max_length=200)
    description = models.TextField()
    steps_to_reproduce = models.TextField(blank=True, default='')
    severity = models.CharField(max_length=20, choices=Severity.choices, default=Severity.MEDIUM)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.OPEN)
    screenshot = models.ImageField(upload_to='bugs/screenshots/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"BUG-{self.id}: {self.title} [{self.get_severity_display()}]"
