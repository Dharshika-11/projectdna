from django.urls import path
from . import views

app_name = 'intelligence'

urlpatterns = [
    path('replay/<slug:slug>/', views.replay_mode_view, name='replay_mode'),
    path('knowledge-graph/<slug:slug>/', views.knowledge_graph_view, name='knowledge_graph'),
    path('vault/', views.knowledge_vault_list, name='vault_list'),
    path('vault/add/', views.knowledge_vault_create, name='vault_create'),
    path('risk-prediction/<slug:slug>/', views.risk_prediction_detail, name='risk_prediction'),
    path('recalculate/<slug:slug>/', views.recalculate_metrics, name='recalculate_metrics'),
]
