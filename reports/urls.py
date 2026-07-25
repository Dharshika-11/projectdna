from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    path('department/', views.department_analytics_report, name='department_analytics'),
    path('archive/', views.semester_archive_list, name='semester_archive'),
    path('project/<slug:slug>/pdf/', views.export_project_pdf_report, name='export_project_pdf'),
]
