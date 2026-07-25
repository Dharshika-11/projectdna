from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from projects.models import Project
from .models import WorkLog, DecisionLog, Task, BugReport

@login_required
def worklog_create(request, slug):
    project = get_object_or_404(Project, slug=slug)
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        hours_spent = request.POST.get('hours_spent', 1.0)
        code_snippet = request.POST.get('code_snippet', '')
        commit_hash = request.POST.get('commit_hash', '')
        
        log = WorkLog.objects.create(
            project=project,
            student=request.user,
            title=title,
            description=description,
            hours_spent=hours_spent,
            code_snippet=code_snippet,
            commit_hash=commit_hash
        )
        if 'screenshot' in request.FILES:
            log.screenshot = request.FILES['screenshot']
        if 'file_attachment' in request.FILES:
            log.file_attachment = request.FILES['file_attachment']
        log.save()
        
        project.update_dna()
        messages.success(request, f"Daily work log '{title}' logged successfully!")
    return redirect('core:project_dashboard', slug=project.slug)

@login_required
def decision_create(request, slug):
    project = get_object_or_404(Project, slug=slug)
    if request.method == 'POST':
        title = request.POST.get('title')
        context = request.POST.get('context')
        decision_taken = request.POST.get('decision_taken')
        consequences = request.POST.get('consequences')
        
        DecisionLog.objects.create(
            project=project,
            author=request.user,
            title=title,
            context=context,
            decision_taken=decision_taken,
            consequences=consequences
        )
        messages.success(request, f"Decision Architectural Record (ADR) '{title}' created!")
    return redirect('core:project_dashboard', slug=project.slug)

@login_required
def task_create(request, slug):
    project = get_object_or_404(Project, slug=slug)
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description', '')
        priority = request.POST.get('priority', 'MEDIUM')
        due_date = request.POST.get('due_date') or None
        
        Task.objects.create(
            project=project,
            created_by=request.user,
            title=title,
            description=description,
            priority=priority,
            due_date=due_date
        )
        messages.success(request, f"Task '{title}' created!")
    return redirect('core:project_dashboard', slug=project.slug)

@login_required
def task_update_status(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        status = request.POST.get('status')
        if status in Task.Status.values:
            task.status = status
            task.save()
            messages.success(request, f"Task '{task.title}' updated to {task.get_status_display()}")
    return redirect('core:project_dashboard', slug=task.project.slug)

@login_required
def bug_report_create(request, slug):
    project = get_object_or_404(Project, slug=slug)
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        steps = request.POST.get('steps_to_reproduce', '')
        severity = request.POST.get('severity', 'MEDIUM')
        
        bug = BugReport.objects.create(
            project=project,
            reported_by=request.user,
            title=title,
            description=description,
            steps_to_reproduce=steps,
            severity=severity
        )
        if 'screenshot' in request.FILES:
            bug.screenshot = request.FILES['screenshot']
            bug.save()
        messages.success(request, f"Bug report BUG-{bug.id} submitted.")
    return redirect('core:project_dashboard', slug=project.slug)

@login_required
def bug_update_status(request, pk):
    bug = get_object_or_404(BugReport, pk=pk)
    if request.method == 'POST':
        status = request.POST.get('status')
        if status in BugReport.Status.values:
            bug.status = status
            if status in ['RESOLVED', 'CLOSED']:
                bug.resolved_at = timezone.now()
            bug.save()
            messages.success(request, f"Bug BUG-{bug.id} status changed to {bug.get_status_display()}")
    return redirect('core:project_dashboard', slug=bug.project.slug)
