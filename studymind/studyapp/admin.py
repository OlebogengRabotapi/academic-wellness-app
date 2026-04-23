"""
Django admin configuration for the study app.
"""
from django.contrib import admin
from .models import StudyMaterial, Summary, PracticeQuestion, ChatMessage, StudySession, UserProfile


@admin.register(StudyMaterial)
class StudyMaterialAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'material_type', 'word_count', 'created_at')
    list_filter = ('material_type', 'created_at')
    search_fields = ('title', 'description', 'user__username')
    readonly_fields = ('created_at', 'updated_at', 'word_count')


@admin.register(Summary)
class SummaryAdmin(admin.ModelAdmin):
    list_display = ('material', 'created_at', 'tokens_used')
    list_filter = ('created_at',)
    search_fields = ('material__title',)
    readonly_fields = ('created_at',)


@admin.register(PracticeQuestion)
class PracticeQuestionAdmin(admin.ModelAdmin):
    list_display = ('material', 'difficulty', 'created_at')
    list_filter = ('difficulty', 'created_at')
    search_fields = ('material__title', 'question')


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('material', 'user', 'created_at', 'tokens_used')
    list_filter = ('created_at',)
    search_fields = ('material__title', 'user__username')
    readonly_fields = ('created_at',)


@admin.register(StudySession)
class StudySessionAdmin(admin.ModelAdmin):
    list_display = ('user', 'material', 'activity_type', 'start_time', 'duration_minutes')
    list_filter = ('activity_type', 'start_time')
    search_fields = ('user__username', 'material__title')


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'study_goal', 'total_study_minutes', 'materials_created')
    search_fields = ('user__username',)
