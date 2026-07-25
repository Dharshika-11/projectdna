from django.test import TestCase, Client
from django.urls import reverse
from accounts.models import Department, User, UserProfile
from projects.models import Project, ProjectMember, Milestone, ProjectDNA
from activity.models import WorkLog, Task, BugReport, DecisionLog
from intelligence.models import KnowledgeVault, ProjectSnapshot, RiskAssessment

class ProjectDNATestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.dept = Department.objects.create(name='Computer Science', code='CS')
        
        self.student = User.objects.create_user(
            username='test_student',
            email='student@nexus.edu',
            password='password123',
            role=User.Role.STUDENT,
            department=self.dept
        )
        UserProfile.objects.create(user=self.student)

        self.faculty = User.objects.create_user(
            username='test_faculty',
            email='faculty@nexus.edu',
            password='password123',
            role=User.Role.FACULTY,
            department=self.dept
        )
        UserProfile.objects.create(user=self.faculty)

        self.project = Project.objects.create(
            title='Autonomous Drone Navigation System',
            abstract='Deep reinforcement learning drone path planning.',
            department=self.dept,
            guide=self.faculty,
            status=Project.Status.IN_PROGRESS
        )
        ProjectMember.objects.create(project=self.project, student=self.student, role_title='Lead Engineer')

    def test_dna_hash_generation(self):
        dna = self.project.update_dna()
        self.assertIsNotNone(dna.dna_hash)
        self.assertEqual(len(dna.dna_hash), 64) # SHA-256 length

    def test_risk_prediction_calculation(self):
        self.client.login(username='test_faculty', password='password123')
        url = reverse('intelligence:risk_prediction', kwargs={'slug': self.project.slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_student_dashboard_access(self):
        self.client.login(username='test_student', password='password123')
        response = self.client.get(reverse('core:student_dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Autonomous Drone Navigation System')

    def test_work_log_submission(self):
        self.client.login(username='test_student', password='password123')
        url = reverse('activity:worklog_create', kwargs={'slug': self.project.slug})
        response = self.client.post(url, {
            'title': 'Implemented Q-Learning Policy Network',
            'description': 'Trained neural network for barrier avoidance.',
            'hours_spent': 3.5,
            'commit_hash': 'ff9988776655'
        })
        self.assertEqual(response.status_code, 302) # Redirect to project dashboard
        self.assertEqual(WorkLog.objects.filter(project=self.project).count(), 1)
