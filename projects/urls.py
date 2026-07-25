from django.urls import path
from . import views

app_name = 'projects'

urlpatterns = [
    path('', views.project_list, name='list'),
    path('create/', views.project_create, name='create'),
    path('<slug:slug>/', views.project_detail, name='detail'),
    path('<slug:slug>/milestones/add/', views.milestone_create, name='milestone_create'),
    path('milestones/<int:pk>/status/', views.milestone_update_status, name='milestone_update_status'),
]
