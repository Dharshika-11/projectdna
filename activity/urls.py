from django.urls import path
from . import views

app_name = 'activity'

urlpatterns = [
    path('worklog/create/<slug:slug>/', views.worklog_create, name='worklog_create'),
    path('decision/create/<slug:slug>/', views.decision_create, name='decision_create'),
    path('task/create/<slug:slug>/', views.task_create, name='task_create'),
    path('task/update/<int:pk>/', views.task_update_status, name='task_update_status'),
    path('bug/report/<slug:slug>/', views.bug_report_create, name='bug_report_create'),
    path('bug/update/<int:pk>/', views.bug_update_status, name='bug_update_status'),
]
