from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from accounts.models import User, Department
from accounts.decorators import student_required, faculty_required, hod_required, admin_required
from projects.models import Project, ProjectMember, ProjectDNA
from activity.models import WorkLog, Task, BugReport
from intelligence.models import KnowledgeVault

def landing_page(request):
    if request.user.is_authenticated:
        return redirect(request.user.get_dashboard_url())

    total_projects = Project.objects.count()
    total_students = User.objects.filter(role=User.Role.STUDENT).count()
    total_departments = Department.objects.count()
    vault_insights = KnowledgeVault.objects.filter(is_public=True).count()

    return render(request, 'core/landing.html', {
        'total_projects': total_projects,
        'total_students': total_students,
        'total_departments': total_departments,
        'vault_insights': vault_insights,
    })

@login_required
def dashboard_redirect(request):
    return redirect(request.user.get_dashboard_url())

@login_required
@student_required
def student_dashboard(request):
    user = request.user
    memberships = ProjectMember.objects.filter(student=user).select_related('project')
    my_projects = [m.project for m in memberships]
    
    my_tasks = Task.objects.filter(assigned_to=user).order_by('-created_at')[:10]
    my_work_logs = WorkLog.objects.filter(student=user).order_by('-date_logged')[:10]
    my_bugs = BugReport.objects.filter(reported_by=user).order_by('-created_at')[:5]

    return render(request, 'core/dashboards/student_dashboard.html', {
        'my_projects': my_projects,
        'my_tasks': my_tasks,
        'my_work_logs': my_work_logs,
        'my_bugs': my_bugs,
    })

@login_required
@faculty_required
def faculty_dashboard(request):
    user = request.user
    guided_projects = Project.objects.filter(guide=user)
    
    pending_proposals = guided_projects.filter(status='PROPOSAL')
    active_projects = guided_projects.filter(status__in=['IN_PROGRESS', 'UNDER_REVIEW'])
    high_risk_projects = guided_projects.filter(risk_level__in=['HIGH', 'CRITICAL'])

    return render(request, 'core/dashboards/faculty_dashboard.html', {
        'guided_projects': guided_projects,
        'pending_proposals': pending_proposals,
        'active_projects': active_projects,
        'high_risk_projects': high_risk_projects,
    })

@login_required
@hod_required
def hod_dashboard(request):
    user = request.user
    department = user.department
    
    dept_projects = Project.objects.filter(department=department) if department else Project.objects.all()
    dept_students = User.objects.filter(role=User.Role.STUDENT, department=department) if department else User.objects.filter(role=User.Role.STUDENT)
    dept_faculty = User.objects.filter(role=User.Role.FACULTY, department=department) if department else User.objects.filter(role=User.Role.FACULTY)

    high_risk_projects = dept_projects.filter(risk_level__in=['HIGH', 'CRITICAL'])
    completed_projects = dept_projects.filter(status='COMPLETED')

    return render(request, 'core/dashboards/hod_dashboard.html', {
        'department': department,
        'dept_projects': dept_projects,
        'dept_students': dept_students,
        'dept_faculty': dept_faculty,
        'high_risk_projects': high_risk_projects,
        'completed_projects': completed_projects,
    })

@login_required
@admin_required
def admin_dashboard(request):
    users = User.objects.all()
    departments = Department.objects.all()
    projects = Project.objects.all()

    student_count = users.filter(role=User.Role.STUDENT).count()
    faculty_count = users.filter(role=User.Role.FACULTY).count()
    hod_count = users.filter(role=User.Role.HOD).count()
    admin_count = users.filter(role=User.Role.ADMIN).count()

    return render(request, 'core/dashboards/admin_dashboard.html', {
        'users': users,
        'departments': departments,
        'projects': projects,
        'student_count': student_count,
        'faculty_count': faculty_count,
        'hod_count': hod_count,
        'admin_count': admin_count,
    })

@login_required
def project_dashboard(request, slug):
    project = get_object_or_404(Project, slug=slug)
    milestones = project.milestones.all()
    work_logs = project.work_logs.all().select_related('student')[:15]
    tasks = project.tasks.all().select_related('assigned_to')[:15]
    bugs = project.bugs.all().select_related('reported_by')[:15]
    decision_logs = project.decision_logs.all().select_related('author')[:10]

    dna, _ = ProjectDNA.objects.get_or_create(project=project)
    if not dna.dna_hash:
        project.update_dna()

    return render(request, 'core/dashboards/project_dashboard.html', {
        'project': project,
        'milestones': milestones,
        'work_logs': work_logs,
        'tasks': tasks,
        'bugs': bugs,
        'decision_logs': decision_logs,
        'dna': dna,
    })

@login_required
def project_dna_dashboard(request, slug):
    project = get_object_or_404(Project, slug=slug)
    dna, _ = ProjectDNA.objects.get_or_create(project=project)
    if not dna.dna_hash:
        dna = project.update_dna()

    vector_dict = dna.get_vector_dict()

    return render(request, 'core/dashboards/project_dna_dashboard.html', {
        'project': project,
        'dna': dna,
        'vector_dict': vector_dict,
    })
