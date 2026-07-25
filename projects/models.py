import hashlib
import json
from django.db import models
from django.utils.text import slugify
from django.utils import timezone
from accounts.models import User, Department

class Project(models.Model):
    class Status(models.TextChoices):
        PROPOSAL = 'PROPOSAL', 'Proposal Submitted'
        IN_PROGRESS = 'IN_PROGRESS', 'In Progress'
        UNDER_REVIEW = 'UNDER_REVIEW', 'Under Review'
        APPROVED = 'APPROVED', 'Approved'
        REJECTED = 'REJECTED', 'Changes Requested'
        COMPLETED = 'COMPLETED', 'Completed & Evaluated'
        ARCHIVED = 'ARCHIVED', 'Archived in Knowledge Vault'

    class RiskLevel(models.TextChoices):
        LOW = 'LOW', 'Low Risk (On Track)'
        MEDIUM = 'MEDIUM', 'Medium Risk (Minor Delays)'
        HIGH = 'HIGH', 'High Risk (Schedules Slipped)'
        CRITICAL = 'CRITICAL', 'Critical Risk (Action Required)'

    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    abstract = models.TextField(help_text="Project scope, objectives, and domain description")
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='projects')
    guide = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={'role': User.Role.FACULTY},
        related_name='guided_projects'
    )
    status = models.CharField(max_length=30, choices=Status.choices, default=Status.PROPOSAL)
    academic_year = models.CharField(max_length=20, default="2025-2026")
    semester = models.IntegerField(default=7)
    github_repo_url = models.URLField(blank=True, null=True)
    
    # Automated Metrics & Analytics
    health_score = models.FloatField(default=85.0, help_text="Dynamic score 0-100 calculated from work logs & milestone velocity")
    innovation_score = models.FloatField(default=75.0, help_text="AI calculated novelty & complexity metric")
    risk_level = models.CharField(max_length=20, choices=RiskLevel.choices, default=RiskLevel.LOW)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while Project.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def compute_dna_fingerprint(self):
        """Generates an immutable SHA-256 fingerprint hash for the project."""
        raw_data = f"{self.id}-{self.title}-{self.created_at}-{self.status}-{self.health_score}-{self.innovation_score}"
        return hashlib.sha256(raw_data.encode('utf-8')).hexdigest().upper()

    def update_dna(self):
        dna, created = ProjectDNA.objects.get_or_create(project=self)
        dna.dna_hash = self.compute_dna_fingerprint()
        dna.generation_count += 1
        
        # Build vector metric breakdown
        metrics = {
            "code_velocity": round(self.health_score * 0.95, 1),
            "review_rigor": round(min(100.0, self.innovation_score * 1.1), 1),
            "bug_resolution": 88.5 if self.risk_level == 'LOW' else (65.0 if self.risk_level == 'MEDIUM' else 40.0),
            "innovation_index": self.innovation_score,
            "documentation_density": 92.0
        }
        dna.vector_data = json.dumps(metrics)
        dna.last_computed_at = timezone.now()
        dna.save()
        return dna

    def __str__(self):
        return f"{self.title} [{self.get_status_display()}]"

    class Meta:
        ordering = ['-updated_at']

class ProjectMember(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='members')
    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'role': User.Role.STUDENT},
        related_name='project_memberships'
    )
    role_title = models.CharField(max_length=100, default='Team Member', help_text='e.g. Lead Architect, UI Developer, Backend Engineer')
    contribution_percentage = models.FloatField(default=0.0)
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('project', 'student')

    def __str__(self):
        return f"{self.student.get_full_name() or self.student.username} -> {self.project.title} ({self.role_title})"

class Milestone(models.Model):
    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        IN_PROGRESS = 'IN_PROGRESS', 'In Progress'
        SUBMITTED = 'SUBMITTED', 'Submitted for Review'
        APPROVED = 'APPROVED', 'Approved'
        REJECTED = 'REJECTED', 'Needs Revision'

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='milestones')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, default='')
    due_date = models.DateField()
    weight_marks = models.IntegerField(default=10, help_text="Internal evaluation weight marks")
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    feedback = models.TextField(blank=True, default='')
    submitted_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.project.title} - {self.title} [{self.get_status_display()}]"

    class Meta:
        ordering = ['due_date']

class ProjectDNA(models.Model):
    project = models.OneToOneField(Project, on_delete=models.CASCADE, related_name='dna')
    dna_hash = models.CharField(max_length=64, blank=True, unique=True)
    generation_count = models.IntegerField(default=1)
    vector_data = models.TextField(default='{}', help_text='JSON metrics vector representation')
    last_computed_at = models.DateTimeField(auto_now=True)

    def get_vector_dict(self):
        try:
            return json.loads(self.vector_data)
        except Exception:
            return {
                "code_velocity": 85.0,
                "review_rigor": 80.0,
                "bug_resolution": 90.0,
                "innovation_index": 75.0,
                "documentation_density": 88.0
            }

    def __str__(self):
        return f"DNA Fingerprint: {self.dna_hash[:16]}... ({self.project.title})"
