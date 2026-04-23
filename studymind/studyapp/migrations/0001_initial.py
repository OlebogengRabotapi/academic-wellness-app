# Generated migration - auto-created by Django
"""
This file is auto-generated. Do not edit manually.
"""
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='StudyMaterial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True)),
                ('content', models.TextField()),
                ('material_type', models.CharField(choices=[('text', 'Text Note'), ('pdf', 'PDF Document'), ('docx', 'Word Document')], default='text', max_length=10)),
                ('file', models.FileField(blank=True, null=True, upload_to='materials/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('word_count', models.IntegerField(default=0)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='study_materials', to='auth.user')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bio', models.TextField(blank=True)),
                ('study_goal', models.CharField(blank=True, max_length=255)),
                ('total_study_minutes', models.IntegerField(default=0)),
                ('materials_created', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to='auth.user')),
            ],
        ),
        migrations.CreateModel(
            name='Summary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('summary_text', models.TextField()),
                ('key_points', models.JSONField(default=list)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('tokens_used', models.IntegerField(default=0)),
                ('material', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='summary', to='studyapp.studymaterial')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='StudySession',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.DateTimeField(auto_now_add=True)),
                ('end_time', models.DateTimeField(blank=True, null=True)),
                ('activity_type', models.CharField(choices=[('reading', 'Reading'), ('quiz', 'Practice Quiz'), ('chat', 'AI Chat'), ('summarizing', 'Summarizing')], max_length=50)),
                ('material', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='studyapp.studymaterial')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='study_sessions', to='auth.user')),
            ],
            options={
                'ordering': ['-start_time'],
            },
        ),
        migrations.CreateModel(
            name='PracticeQuestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.TextField()),
                ('answer', models.TextField()),
                ('difficulty', models.CharField(choices=[('easy', 'Easy'), ('medium', 'Medium'), ('hard', 'Hard')], default='medium', max_length=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('material', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='practice_questions', to='studyapp.studymaterial')),
            ],
            options={
                'ordering': ['difficulty', '-created_at'],
            },
        ),
        migrations.CreateModel(
            name='ChatMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_message', models.TextField()),
                ('ai_response', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('tokens_used', models.IntegerField(default=0)),
                ('material', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='chat_messages', to='studyapp.studymaterial')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth.user')),
            ],
            options={
                'ordering': ['created_at'],
            },
        ),
    ]
