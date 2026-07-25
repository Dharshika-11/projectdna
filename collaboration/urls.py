from django.urls import path
from . import views

app_name = 'collaboration'

urlpatterns = [
    path('chat/<slug:slug>/', views.project_chat, name='project_chat'),
    path('chat/<slug:slug>/send/', views.send_chat_message, name='send_chat_message'),
    path('notifications/', views.notifications_list, name='notifications_list'),
    path('notifications/mark-read/<int:pk>/', views.mark_notification_read, name='mark_notification_read'),
    path('forum/<slug:slug>/', views.discussion_forum, name='discussion_forum'),
    path('forum/<slug:slug>/topic/create/', views.create_topic, name='create_topic'),
]
