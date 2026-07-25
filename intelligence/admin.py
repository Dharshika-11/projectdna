from django.contrib import admin
from .models import KnowledgeVault, ProjectSnapshot, RiskAssessment, ContributionScore

admin.site.register(KnowledgeVault)
admin.site.register(ProjectSnapshot)
admin.site.register(RiskAssessment)
admin.site.register(ContributionScore)
