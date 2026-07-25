from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.landing_page, name='landing'),
    path('dashboard/', views.dashboard_redirect, name='dashboard'),
    path('dashboard/student/', views.student_dashboard, name='student_dashboard'),
    path('dashboard/faculty/', views.faculty_dashboard, name='faculty_dashboard'),
    path('dashboard/hod/', views.hod_dashboard, name='hod_dashboard'),
    path('dashboard/admin/', views.admin_dashboard, name='admin_dashboard'),
    path('project/<slug:slug>/dashboard/', views.project_dashboard, name='project_dashboard'),
    path('project/<slug:slug>/dna/', views.project_dna_dashboard, name='project_dna_dashboard'),
]
