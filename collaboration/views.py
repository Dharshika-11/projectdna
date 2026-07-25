from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
from projects.models import Project
from .models import ChatMessage, Notification, DiscussionTopic, DiscussionReply

@login_required
def project_chat(request, slug):
    project = get_object_or_404(Project, slug=slug)
    chat_messages = project.chat_messages.all().select_related('sender')[:50]
    return render(request, 'collaboration/project_chat.html', {
        'project': project,
        'chat_messages': chat_messages,
    })

@login_required
def send_chat_message(request, slug):
    project = get_object_or_404(Project, slug=slug)
    if request.method == 'POST':
        message_text = request.POST.get('message', '').strip()
        if message_text:
            msg = ChatMessage.objects.create(
                project=project,
                sender=request.user,
                message=message_text
            )
            if 'attachment' in request.FILES:
                msg.attachment = request.FILES['attachment']
                msg.save()
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'status': 'ok', 'id': msg.id, 'sender': msg.sender.username, 'timestamp': msg.timestamp.strftime('%H:%M'), 'message': msg.message})
            messages.success(request, "Message sent to team chat.")
            return redirect('collaboration:project_chat', slug=project.slug)
    return redirect('collaboration:project_chat', slug=project.slug)

@login_required
def notifications_list(request):
    notifications = Notification.objects.filter(recipient=request.user)
    return render(request, 'collaboration/notifications_list.html', {'notifications': notifications})

@login_required
def mark_notification_read(request, pk):
    notif = get_object_or_404(Notification, pk=pk, recipient=request.user)
    notif.is_read = True
    notif.save()
    if notif.link_url and notif.link_url != '#':
        return redirect(notif.link_url)
    return redirect('collaboration:notifications_list')

@login_required
def discussion_forum(request, slug):
    project = get_object_or_404(Project, slug=slug)
    topics = project.discussions.all()
    return render(request, 'collaboration/discussion_forum.html', {
        'project': project,
        'topics': topics,
    })

@login_required
def create_topic(request, slug):
    project = get_object_or_404(Project, slug=slug)
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        if title and content:
            DiscussionTopic.objects.create(
                project=project,
                author=request.user,
                title=title,
                content=content
            )
            messages.success(request, f"Discussion topic '{title}' created.")
    return redirect('collaboration:discussion_forum', slug=project.slug)
