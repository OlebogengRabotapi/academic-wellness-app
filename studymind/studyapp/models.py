"""
Models for the study app.
"""
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class StudyMaterial(models.Model):
    """Model to store study materials uploaded by users."""
    MATERIAL_TYPES = (
        ('text', 'Text Note'),
        ('pdf', 'PDF Document'),
        ('docx', 'Word Document'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='study_materials')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    content = models.TextField()  # Stores the actual text content
    material_type = models.CharField(max_length=10, choices=MATERIAL_TYPES, default='text')
    file = models.FileField(upload_to='materials/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    word_count = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    def update_word_count(self):
        """Update the word count based on content."""
        self.word_count = len(self.content.split())
        self.save()


class Summary(models.Model):
    """Model to store AI-generated summaries of study materials."""
    material = models.OneToOneField(StudyMaterial, on_delete=models.CASCADE, related_name='summary')
    summary_text = models.TextField()
    key_points = models.JSONField(default=list)  # Store as list of strings
    created_at = models.DateTimeField(auto_now_add=True)
    tokens_used = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Summary of {self.material.title}"


class PracticeQuestion(models.Model):
    """Model to store AI-generated practice questions."""
    DIFFICULTY_LEVELS = (
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    )
    
    material = models.ForeignKey(StudyMaterial, on_delete=models.CASCADE, related_name='practice_questions')
    question = models.TextField()
    answer = models.TextField()
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_LEVELS, default='medium')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['difficulty', '-created_at']
    
    def __str__(self):
        return f"Question for {self.material.title}"


class ChatMessage(models.Model):
    """Model to store chat conversations between user and AI."""
    material = models.ForeignKey(StudyMaterial, on_delete=models.CASCADE, related_name='chat_messages')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_message = models.TextField()
    ai_response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    tokens_used = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['created_at']
    
    def __str__(self):
        return f"Chat on {self.material.title} at {self.created_at}"


class StudySession(models.Model):
    """Model to track user study sessions."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='study_sessions')
    material = models.ForeignKey(StudyMaterial, on_delete=models.SET_NULL, null=True, blank=True)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    activity_type = models.CharField(
        max_length=50,
        choices=[
            ('reading', 'Reading'),
            ('quiz', 'Practice Quiz'),
            ('chat', 'AI Chat'),
            ('summarizing', 'Summarizing'),
        ]
    )
    
    class Meta:
        ordering = ['-start_time']
    
    def __str__(self):
        return f"{self.user.username} - {self.activity_type}"
    
    @property
    def duration_minutes(self):
        """Calculate duration in minutes."""
        if self.end_time:
            return int((self.end_time - self.start_time).total_seconds() / 60)
        return 0


class UserProfile(models.Model):
    """Extended user profile for tracking study stats."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True)
    study_goal = models.CharField(max_length=255, blank=True)
    total_study_minutes = models.IntegerField(default=0)
    materials_created = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username}'s Profile"
