import json
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from accounts.models import Department, User, UserProfile
from projects.models import Project, ProjectMember, Milestone, ProjectDNA
from activity.models import WorkLog, DecisionLog, Task, BugReport
from intelligence.models import KnowledgeVault, ProjectSnapshot, RiskAssessment, ContributionScore

class Command(BaseCommand):
    help = 'Seeds initial demonstration data for PROJECTDNA NEXUS'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Starting database seeding process..."))

        # 1. Create Departments
        cs_dept, _ = Department.objects.get_or_create(
            code='CS',
            defaults={'name': 'Department of Computer Science', 'description': 'Advanced computing & system engineering'}
        )
        se_dept, _ = Department.objects.get_or_create(
            code='SE',
            defaults={'name': 'Department of Software Engineering', 'description': 'Full-stack & cloud architecture'}
        )

        # 2. Create Users (Admin, HOD, Faculty, Students)
        admin_user, _ = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@nexus.edu',
                'first_name': 'System',
                'last_name': 'Administrator',
                'role': User.Role.ADMIN,
                'is_staff': True,
                'is_superuser': True,
                'department': cs_dept,
            }
        )
        admin_user.set_password('admin123')
        admin_user.save()
        UserProfile.objects.get_or_create(user=admin_user, defaults={'bio': 'Enterprise System Administrator'})

        hod_user, _ = User.objects.get_or_create(
            username='hod_cs',
            defaults={
                'email': 'hod@nexus.edu',
                'first_name': 'Dr. Alan',
                'last_name': 'Turing',
                'role': User.Role.HOD,
                'department': cs_dept,
                'designation': 'Head of Department - Computer Science',
            }
        )
        hod_user.set_password('hod123')
        hod_user.save()
        UserProfile.objects.get_or_create(user=hod_user, defaults={'bio': 'HOD Computer Science Department'})

        faculty_user, _ = User.objects.get_or_create(
            username='dr_smith',
            defaults={
                'email': 'smith@nexus.edu',
                'first_name': 'Dr. Sarah',
                'last_name': 'Smith',
                'role': User.Role.FACULTY,
                'department': cs_dept,
                'designation': 'Associate Professor & Senior Project Advisor',
            }
        )
        faculty_user.set_password('faculty123')
        faculty_user.save()
        UserProfile.objects.get_or_create(user=faculty_user, defaults={'bio': 'Research Advisor in Distributed Systems & AI'})

        student1, _ = User.objects.get_or_create(
            username='alex_student',
            defaults={
                'email': 'alex@nexus.edu',
                'first_name': 'Alex',
                'last_name': 'Mercer',
                'role': User.Role.STUDENT,
                'department': cs_dept,
                'roll_number': '2024-CS-01',
            }
        )
        student1.set_password('student123')
        student1.save()
        UserProfile.objects.get_or_create(user=student1, defaults={'bio': 'Lead Full-Stack Developer | Python & React Specialist', 'skills': 'Python, Django, React, PostgreSQL'})

        student2, _ = User.objects.get_or_create(
            username='maria_student',
            defaults={
                'email': 'maria@nexus.edu',
                'first_name': 'Maria',
                'last_name': 'Garcia',
                'role': User.Role.STUDENT,
                'department': cs_dept,
                'roll_number': '2024-CS-02',
            }
        )
        student2.set_password('student123')
        student2.save()
        UserProfile.objects.get_or_create(user=student2, defaults={'bio': 'UI/UX & Backend Engineer', 'skills': 'HTML5, Bootstrap, Python, SQLite'})

        # 3. Create Sample Project
        project, created = Project.objects.get_or_create(
            slug='projectdna-nexus-platform',
            defaults={
                'title': 'PROJECTDNA NEXUS Platform',
                'abstract': 'Intelligent Academic Project Lifecycle & Evolution Platform recording decisions, contributions, DNA fingerprints, replay timelines, and delay risk predictions.',
                'department': cs_dept,
                'guide': faculty_user,
                'status': Project.Status.IN_PROGRESS,
                'academic_year': '2025-2026',
                'semester': 7,
                'github_repo_url': 'https://github.com/academic/projectdna-nexus',
                'health_score': 92.5,
                'innovation_score': 88.0,
                'risk_level': Project.RiskLevel.LOW,
            }
        )

        # 4. Project Members
        ProjectMember.objects.get_or_create(project=project, student=student1, defaults={'role_title': 'Lead Software Architect', 'contribution_percentage': 60.0})
        ProjectMember.objects.get_or_create(project=project, student=student2, defaults={'role_title': 'UI/UX & Database Engineer', 'contribution_percentage': 40.0})

        # 5. Milestones
        today = timezone.now().date()
        m1, _ = Milestone.objects.get_or_create(
            project=project,
            title='Phase 1: Architecture & Data Schema Specification',
            defaults={
                'description': 'Finalize core app structure, Custom User model, and RBAC authentication permissions.',
                'due_date': today - timedelta(days=15),
                'weight_marks': 20,
                'status': Milestone.Status.APPROVED,
                'completed_at': timezone.now() - timedelta(days=15),
                'feedback': 'Excellent architectural document and complete database schema design.'
            }
        )

        m2, _ = Milestone.objects.get_or_create(
            project=project,
            title='Phase 2: Core Dashboards & Advanced Intelligence Engines',
            defaults={
                'description': 'Develop Student, Faculty, HOD, and Admin dashboards along with Replay Engine and DNA Hash calculation.',
                'due_date': today + timedelta(days=10),
                'weight_marks': 40,
                'status': Milestone.Status.IN_PROGRESS,
            }
        )

        # 6. Work Logs
        WorkLog.objects.get_or_create(
            project=project,
            student=student1,
            title='Implemented Custom User Model & RBAC Mixins',
            defaults={
                'description': 'Created custom user model extending AbstractUser with 4 explicit roles (Student, Faculty, HOD, Admin) and security mixins.',
                'hours_spent': 4.5,
                'commit_hash': 'a1b2c3d4e5f6',
                'code_snippet': 'class User(AbstractUser):\n    class Role(models.TextChoices):\n        STUDENT = "STUDENT"\n        FACULTY = "FACULTY"',
            }
        )

        WorkLog.objects.get_or_create(
            project=project,
            student=student2,
            title='Designed Modern Dashboard Glassmorphism UI',
            defaults={
                'description': 'Integrated Bootstrap 5, Font Awesome, and dynamic dark CSS variable palette for high-impact visual aesthetics.',
                'hours_spent': 5.0,
                'commit_hash': 'f6e5d4c3b2a1',
            }
        )

        # 7. Decision Log (ADR)
        DecisionLog.objects.get_or_create(
            project=project,
            title='Adopted Monolithic Modular Django App Architecture',
            defaults={
                'author': student1,
                'context': 'Need clean separation of concerns for projects, activity logs, intelligence metrics, and reports without microservice overhead.',
                'decision_taken': 'Organized domain into core, accounts, projects, activity, intelligence, collaboration, and reports apps.',
                'consequences': 'High cohesion, easy testability, simplified deployment with full Django ORM capabilities.',
                'status': DecisionLog.Status.ACCEPTED,
            }
        )

        # 8. Tasks & Bug Reports
        Task.objects.get_or_create(
            project=project,
            title='Integrate Dynamic Chart.js Metrics on HOD Dashboard',
            defaults={
                'created_by': faculty_user,
                'assigned_to': student2,
                'priority': Task.Priority.HIGH,
                'status': Task.Status.IN_PROGRESS,
            }
        )

        BugReport.objects.get_or_create(
            project=project,
            title='Chart canvas initial height overflow on mobile breakpoint',
            defaults={
                'reported_by': student2,
                'assigned_to': student2,
                'severity': BugReport.Severity.LOW,
                'status': BugReport.Status.RESOLVED,
                'steps_to_reproduce': 'Resize screen to 375px width in mobile browser view.',
            }
        )

        # 9. Knowledge Vault Entry
        KnowledgeVault.objects.get_or_create(
            title='Optimizing Dynamic SHA-256 DNA Hash Generation in Django',
            defaults={
                'author': faculty_user,
                'category': KnowledgeVault.Category.BEST_PRACTICE,
                'content': 'Always compute project SHA-256 fingerprints after critical model mutations (work log submission, milestone approvals) to maintain immutable chain integrity.',
                'tags': 'SHA-256, Django ORM, DNA Engine, Security',
                'is_public': True,
            }
        )

        # 10. Update DNA & Replay Snapshots
        project.update_dna()

        self.stdout.write(self.style.SUCCESS("Database seeding completed successfully!"))
        self.stdout.write(self.style.SUCCESS("Demo Accounts Created:"))
        self.stdout.write("  - Admin:    admin / admin123")
        self.stdout.write("  - HOD:      hod_cs / hod123")
        self.stdout.write("  - Faculty:  dr_smith / faculty123")
        self.stdout.write("  - Student 1: alex_student / student123")
        self.stdout.write("  - Student 2: maria_student / student123")
