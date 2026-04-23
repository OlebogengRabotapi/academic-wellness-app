"""
URL configuration for the study app.
"""
from django.urls import path
from . import views

app_name = 'studyapp'

urlpatterns = [
    # Authentication
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Public
    path('', views.home, name='home'),
    
    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),
    path('stats/', views.study_stats, name='study_stats'),
    
    # Study Materials
    path('materials/', views.material_list, name='material_list'),
    path('material/create/', views.create_material, name='create_material'),
    path('material/<int:pk>/', views.material_detail, name='material_detail'),
    path('material/<int:pk>/edit/', views.edit_material, name='edit_material'),
    path('material/<int:pk>/delete/', views.delete_material, name='delete_material'),
    
    # AI Features
    path('material/<int:pk>/summary/generate/', views.generate_summary, name='generate_summary'),
    path('material/<int:pk>/questions/generate/', views.generate_questions, name='generate_questions'),
    path('material/<int:pk>/chat/', views.chat_message, name='chat_message'),
    path('material/<int:pk>/chat/history/', views.chat_history, name='chat_history'),
    
    # Study Sessions
    path('session/start/<int:pk>/', views.start_session, name='start_session'),
    path('session/end/', views.end_session, name='end_session'),
    
    # API Endpoints
    path('api/material/<int:pk>/summary/', views.api_material_summary, name='api_material_summary'),
]
