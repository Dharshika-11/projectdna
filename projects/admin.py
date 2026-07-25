from django.contrib import admin
from .models import Project, ProjectMember, Milestone, ProjectDNA

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'department', 'status', 'health_score', 'innovation_score', 'risk_level')
    list_filter = ('status', 'risk_level', 'department', 'academic_year')
    search_fields = ('title', 'abstract', 'slug')
    prepopulated_fields = {'slug': ('title',)}

admin.site.register(ProjectMember)
admin.site.register(Milestone)
admin.site.register(ProjectDNA)
