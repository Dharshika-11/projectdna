from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Project, ProjectMember, Milestone

@login_required
def project_list(request):
    projects = Project.objects.all()
    return render(request, 'projects/project_list.html', {'projects': projects})

@login_required
def project_create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        abstract = request.POST.get('abstract')
        github_repo_url = request.POST.get('github_repo_url')
        if title and abstract:
            project = Project.objects.create(
                title=title,
                abstract=abstract,
                department=request.user.department if request.user.department else None,
                github_repo_url=github_repo_url
            )
            ProjectMember.objects.create(project=project, student=request.user, role_title='Lead Developer', contribution_percentage=100.0)
            project.update_dna()
            messages.success(request, f"Project '{project.title}' created successfully!")
            return redirect('core:project_dashboard', slug=project.slug)
    return render(request, 'projects/project_create.html')

@login_required
def project_detail(request, slug):
    project = get_object_or_404(Project, slug=slug)
    return render(request, 'projects/project_detail.html', {'project': project})

@login_required
def milestone_create(request, slug):
    project = get_object_or_404(Project, slug=slug)
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description', '')
        due_date = request.POST.get('due_date')
        weight_marks = request.POST.get('weight_marks', 10)
        if title and due_date:
            Milestone.objects.create(
                project=project,
                title=title,
                description=description,
                due_date=due_date,
                weight_marks=weight_marks
            )
            messages.success(request, f"Milestone '{title}' added to {project.title}.")
    return redirect('core:project_dashboard', slug=project.slug)

@login_required
def milestone_update_status(request, pk):
    milestone = get_object_or_404(Milestone, pk=pk)
    if request.method == 'POST':
        status = request.POST.get('status')
        feedback = request.POST.get('feedback', '')
        if status in Milestone.Status.values:
            milestone.status = status
            if feedback:
                milestone.feedback = feedback
            milestone.save()
            messages.success(request, f"Milestone '{milestone.title}' updated to {milestone.get_status_display()}.")
    return redirect('core:project_dashboard', slug=milestone.project.slug)
