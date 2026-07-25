from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from accounts.models import Department, User
from projects.models import Project
from .models import SemesterArchive

@login_required
def department_analytics_report(request):
    user = request.user
    department = user.department if user.department else Department.objects.first()
    
    projects = Project.objects.filter(department=department) if department else Project.objects.all()
    students_count = User.objects.filter(role=User.Role.STUDENT, department=department).count() if department else 0
    faculty_count = User.objects.filter(role=User.Role.FACULTY, department=department).count() if department else 0

    active_count = projects.filter(status__in=['IN_PROGRESS', 'UNDER_REVIEW']).count()
    completed_count = projects.filter(status='COMPLETED').count()
    high_risk_count = projects.filter(risk_level__in=['HIGH', 'CRITICAL']).count()

    return render(request, 'reports/department_analytics.html', {
        'department': department,
        'projects': projects,
        'students_count': students_count,
        'faculty_count': faculty_count,
        'active_count': active_count,
        'completed_count': completed_count,
        'high_risk_count': high_risk_count,
    })

@login_required
def semester_archive_list(request):
    archives = SemesterArchive.objects.all()
    return render(request, 'reports/semester_archive.html', {'archives': archives})

@login_required
def export_project_pdf_report(request, slug):
    project = get_object_or_404(Project, slug=slug)
    # Simple plain text or print layout summary for PDF export fallback
    html_content = f"""
    ===============================================================
    PROJECTDNA NEXUS - IMMUTABLE EXECUTIVE SUMMARY REPORT
    ===============================================================
    Project Title: {project.title}
    Department: {project.department.name if project.department else 'General'}
    Status: {project.get_status_display()}
    Academic Year: {project.academic_year} (Semester {project.semester})
    Health Score: {project.health_score}% | Innovation Score: {project.innovation_score}%
    Risk Level: {project.get_risk_level_display()}
    DNA Fingerprint Hash: {project.compute_dna_fingerprint()}
    
    Team Members:
    """
    for m in project.members.all():
        html_content += f"  - {m.student.get_full_name() or m.student.username} ({m.role_title})\n"

    response = HttpResponse(html_content, content_type='text/plain')
    response['Content-Disposition'] = f'attachment; filename="ProjectDNA_Report_{project.slug}.txt"'
    return response
