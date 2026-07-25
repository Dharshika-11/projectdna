import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from projects.models import Project
from .models import KnowledgeVault, ProjectSnapshot, RiskAssessment

@login_required
def replay_mode_view(request, slug):
    project = get_object_or_404(Project, slug=slug)
    snapshots = project.snapshots.all().order_by('version_number')
    
    # If no snapshots exist yet, build initial historical snapshots dynamically
    if not snapshots.exists():
        ProjectSnapshot.objects.create(
            project=project,
            version_number=1,
            health_score=70.0,
            innovation_score=65.0,
            total_work_logs=1,
            summary_note="Initial Project Proposal and Scope Approval",
            snapshot_json=json.dumps({"phase": "Proposal", "milestones_done": 0, "active_bugs": 0})
        )
        ProjectSnapshot.objects.create(
            project=project,
            version_number=2,
            health_score=82.0,
            innovation_score=75.0,
            total_work_logs=3,
            summary_note="Architecture Specification & Database Schema Initialization",
            snapshot_json=json.dumps({"phase": "Design", "milestones_done": 1, "active_bugs": 1})
        )
        ProjectSnapshot.objects.create(
            project=project,
            version_number=3,
            health_score=project.health_score,
            innovation_score=project.innovation_score,
            total_work_logs=project.work_logs.count(),
            summary_note="Current Active Evolution State",
            snapshot_json=json.dumps({"phase": "Active Development", "milestones_done": project.milestones.filter(status='APPROVED').count(), "active_bugs": project.bugs.filter(status='OPEN').count()})
        )
        snapshots = project.snapshots.all().order_by('version_number')

    return render(request, 'intelligence/replay_mode.html', {
        'project': project,
        'snapshots': snapshots,
    })

@login_required
def knowledge_graph_view(request, slug):
    project = get_object_or_404(Project, slug=slug)
    
    # Build graph nodes and links JSON payload for UI rendering
    nodes = [
        {"id": f"P-{project.id}", "label": project.title, "type": "project", "color": "#4e73df"},
    ]
    links = []
    
    for member in project.members.all():
        m_id = f"U-{member.student.id}"
        nodes.append({"id": m_id, "label": member.student.get_full_name() or member.student.username, "type": "student", "color": "#1cc88a"})
        links.append({"source": m_id, "target": f"P-{project.id}", "label": member.role_title})

    for milestone in project.milestones.all():
        ms_id = f"MS-{milestone.id}"
        nodes.append({"id": ms_id, "label": milestone.title, "type": "milestone", "color": "#f6c23e"})
        links.append({"source": f"P-{project.id}", "target": ms_id, "label": "milestone"})

    for bug in project.bugs.all()[:5]:
        b_id = f"BUG-{bug.id}"
        nodes.append({"id": b_id, "label": f"BUG-{bug.id}: {bug.title[:15]}", "type": "bug", "color": "#e74a3b"})
        links.append({"source": b_id, "target": f"P-{project.id}", "label": "issue"})

    graph_data = json.dumps({"nodes": nodes, "links": links})

    return render(request, 'intelligence/knowledge_graph.html', {
        'project': project,
        'graph_data': graph_data,
    })

@login_required
def knowledge_vault_list(request):
    category_filter = request.GET.get('category', '')
    entries = KnowledgeVault.objects.filter(is_public=True)
    if category_filter:
        entries = entries.filter(category=category_filter)
    return render(request, 'intelligence/vault_list.html', {
        'entries': entries,
        'category_filter': category_filter,
    })

@login_required
def knowledge_vault_create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        category = request.POST.get('category', 'LESSON_LEARNED')
        content = request.POST.get('content')
        tags = request.POST.get('tags', '')
        
        entry = KnowledgeVault.objects.create(
            author=request.user,
            title=title,
            category=category,
            content=content,
            tags=tags
        )
        messages.success(request, f"Knowledge Vault entry '{entry.title}' published!")
        return redirect('intelligence:vault_list')
    return render(request, 'intelligence/vault_create.html')

@login_required
def risk_prediction_detail(request, slug):
    project = get_object_or_404(Project, slug=slug)
    
    # Calculate automated delay risk score & factors
    factors = []
    recommendations = []
    risk_score = 15.0 # baseline low
    
    pending_milestones = project.milestones.filter(status__in=['PENDING', 'IN_PROGRESS'])
    overdue_milestones = [m for m in pending_milestones if m.due_date < timezone.now().date()]
    
    if overdue_milestones:
        risk_score += 35.0
        factors.append(f"Overdue Milestones: {len(overdue_milestones)} pending milestone(s) passed scheduled due date.")
        recommendations.append("Faculty Guide intervention recommended to re-scope pending milestone deliverables.")

    open_critical_bugs = project.bugs.filter(severity__in=['HIGH', 'CRITICAL'], status='OPEN').count()
    if open_critical_bugs > 0:
        risk_score += 25.0
        factors.append(f"Unresolved Critical Bugs: {open_critical_bugs} high/critical severity defect(s) currently open.")
        recommendations.append("Prioritize defect resolution sprint before advancing feature scope.")

    work_logs_count = project.work_logs.count()
    if work_logs_count < 3:
        risk_score += 20.0
        factors.append("Low Work Logging Velocity: Infrequent daily work log activity detected.")
        recommendations.append("Enforce mandatory daily work log entries for all assigned student team members.")

    risk_score = min(99.0, risk_score)
    
    if risk_score > 70.0:
        category = Project.RiskLevel.CRITICAL
        predicted_delay = 14
    elif risk_score > 45.0:
        category = Project.RiskLevel.HIGH
        predicted_delay = 7
    elif risk_score > 25.0:
        category = Project.RiskLevel.MEDIUM
        predicted_delay = 3
    else:
        category = Project.RiskLevel.LOW
        predicted_delay = 0

    project.risk_level = category
    project.save()

    assessment = RiskAssessment.objects.create(
        project=project,
        risk_score=risk_score,
        risk_category=category,
        predicted_delay_days=predicted_delay,
        risk_factors_json=json.dumps(factors),
        recommendations_json=json.dumps(recommendations)
    )

    return render(request, 'intelligence/risk_prediction.html', {
        'project': project,
        'assessment': assessment,
        'factors': factors,
        'recommendations': recommendations,
    })

@login_required
def recalculate_metrics(request, slug):
    project = get_object_or_404(Project, slug=slug)
    project.update_dna()
    messages.success(request, f"DNA Fingerprint and health scores recalculated for {project.title}.")
    return redirect('core:project_dna_dashboard', slug=project.slug)
