"""
Views for the study app.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.contrib import messages
from django.db.models import Q, Count
from django.utils import timezone

from .models import StudyMaterial, Summary, PracticeQuestion, ChatMessage, StudySession, UserProfile
from .forms import UserRegistrationForm, StudyMaterialForm, ChatForm
from .ai_service import ai_service
import json

# ============================================================================
# Authentication Views
# ============================================================================

def register(request):
    """Handle user registration."""
    if request.user.is_authenticated:
        return redirect('studyapp:dashboard')
    
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create user profile
            UserProfile.objects.create(user=user)
            login(request, user)
            messages.success(request, 'Registration successful! Welcome to StudyMind.')
            return redirect('studyapp:dashboard')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = UserRegistrationForm()
    
    return render(request, 'auth/register.html', {'form': form})


def login_view(request):
    """Handle user login."""
    if request.user.is_authenticated:
        return redirect('studyapp:dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {username}!')
            return redirect('studyapp:dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'auth/login.html')


def logout_view(request):
    """Handle user logout."""
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('studyapp:home')


# ============================================================================
# Public Views
# ============================================================================

def home(request):
    """Homepage with project information."""
    if request.user.is_authenticated:
        return redirect('studyapp:dashboard')
    
    stats = {
        'total_users': UserProfile.objects.count(),
        'total_materials': StudyMaterial.objects.count(),
        'total_summaries': Summary.objects.count(),
    }
    return render(request, 'home.html', stats)


# ============================================================================
# Dashboard & Core Functionality
# ============================================================================

@login_required(login_url='studyapp:login')
def dashboard(request):
    """User dashboard showing overview and recent activities."""
    user = request.user
    
    # Get user's study materials
    materials = StudyMaterial.objects.filter(user=user).order_by('-created_at')[:5]
    
    # Get recent study sessions
    sessions = StudySession.objects.filter(user=user).order_by('-start_time')[:5]
    
    # Calculate stats
    total_materials = StudyMaterial.objects.filter(user=user).count()
    
    # Get user profile
    profile, _ = UserProfile.objects.get_or_create(user=user)
    
    context = {
        'materials': materials,
        'sessions': sessions,
        'total_materials': total_materials,
        'profile': profile,
    }
    
    return render(request, 'dashboard.html', context)


@login_required(login_url='studyapp:login')
def create_material(request):
    """Create a new study material."""
    if request.method == 'POST':
        form = StudyMaterialForm(request.POST, request.FILES)
        if form.is_valid():
            material = form.save(commit=False)
            material.user = request.user
            material.save()
            
            # Update word count
            material.update_word_count()
            
            # Track in user profile
            profile = UserProfile.objects.get(user=request.user)
            profile.materials_created += 1
            profile.save()
            
            messages.success(request, 'Study material created successfully!')
            return redirect('studyapp:material_detail', pk=material.pk)
    else:
        form = StudyMaterialForm()
    
    return render(request, 'material/create.html', {'form': form})


@login_required(login_url='studyapp:login')
def material_detail(request, pk):
    """View details of a study material."""
    material = get_object_or_404(StudyMaterial, pk=pk, user=request.user)
    summary = Summary.objects.filter(material=material).first()
    questions = PracticeQuestion.objects.filter(material=material)
    chat_form = ChatForm()
    
    context = {
        'material': material,
        'summary': summary,
        'questions': questions,
        'chat_form': chat_form,
    }
    
    return render(request, 'material/detail.html', context)


@login_required(login_url='studyapp:login')
def material_list(request):
    """List all user's study materials."""
    materials = StudyMaterial.objects.filter(user=request.user).order_by('-created_at')
    
    # Search functionality
    query = request.GET.get('q')
    if query:
        materials = materials.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )
    
    context = {
        'materials': materials,
        'query': query,
    }
    
    return render(request, 'material/list.html', context)


@login_required(login_url='studyapp:login')
def edit_material(request, pk):
    """Edit a study material."""
    material = get_object_or_404(StudyMaterial, pk=pk, user=request.user)
    
    if request.method == 'POST':
        form = StudyMaterialForm(request.POST, request.FILES, instance=material)
        if form.is_valid():
            material = form.save()
            material.update_word_count()
            messages.success(request, 'Material updated successfully!')
            return redirect('studyapp:material_detail', pk=material.pk)
    else:
        form = StudyMaterialForm(instance=material)
    
    return render(request, 'material/edit.html', {'form': form, 'material': material})


@login_required(login_url='studyapp:login')
def delete_material(request, pk):
    """Delete a study material."""
    material = get_object_or_404(StudyMaterial, pk=pk, user=request.user)
    
    if request.method == 'POST':
        material.delete()
        messages.success(request, 'Material deleted successfully!')
        return redirect('studyapp:material_list')
    
    return render(request, 'material/delete_confirm.html', {'material': material})


# ============================================================================
# AI Features
# ============================================================================

@login_required(login_url='studyapp:login')
@require_http_methods(["POST"])
def generate_summary(request, pk):
    """Generate AI summary for a study material."""
    material = get_object_or_404(StudyMaterial, pk=pk, user=request.user)
    
    # Check if summary already exists
    if Summary.objects.filter(material=material).exists():
        messages.warning(request, 'Summary already exists for this material.')
        return redirect('studyapp:material_detail', pk=material.pk)
    
    # Generate summary using AI
    result = ai_service.generate_summary(material.content, material.title)
    
    if result['success']:
        summary = Summary.objects.create(
            material=material,
            summary_text=result['summary'],
            key_points=result['key_points'],
            tokens_used=0,
        )
        messages.success(request, 'Summary generated successfully!')
    else:
        messages.error(request, f'Error generating summary: {result.get("error", "Unknown error")}')
    
    return redirect('studyapp:material_detail', pk=material.pk)


@login_required(login_url='studyapp:login')
@require_http_methods(["POST"])
def generate_questions(request, pk):
    """Generate practice questions for a study material."""
    material = get_object_or_404(StudyMaterial, pk=pk, user=request.user)
    
    # Check if questions already exist
    if PracticeQuestion.objects.filter(material=material).exists():
        messages.warning(request, 'Questions already exist for this material.')
        return redirect('studyapp:material_detail', pk=material.pk)
    
    # Generate questions using AI
    result = ai_service.generate_practice_questions(material.content, material.title, num_questions=5)
    
    if result['success']:
        for q_data in result['questions']:
            PracticeQuestion.objects.create(
                material=material,
                question=q_data.get('question', 'Question'),
                answer=q_data.get('answer', 'Answer'),
                difficulty=q_data.get('difficulty', 'medium'),
            )
        messages.success(request, f'Generated {len(result["questions"])} practice questions!')
    else:
        messages.error(request, f'Error generating questions: {result.get("error", "Unknown error")}')
    
    return redirect('studyapp:material_detail', pk=material.pk)


@login_required(login_url='studyapp:login')
@require_http_methods(["POST"])
def chat_message(request, pk):
    """Handle chat message for AI tutoring."""
    material = get_object_or_404(StudyMaterial, pk=pk, user=request.user)
    
    form = ChatForm(request.POST)
    if form.is_valid():
        user_message = form.cleaned_data['message']
        
        # Get AI response
        result = ai_service.answer_question(user_message, material.content, material.title)
        
        if result['success']:
            chat = ChatMessage.objects.create(
                material=material,
                user=request.user,
                user_message=user_message,
                ai_response=result['answer'],
                tokens_used=0,
            )
            messages.success(request, 'Question answered by AI tutor!')
        else:
            messages.error(request, f'Error getting response: {result.get("error", "Unknown error")}')
    
    return redirect('studyapp:material_detail', pk=material.pk)


@login_required(login_url='studyapp:login')
def chat_history(request, pk):
    """View chat history for a study material."""
    material = get_object_or_404(StudyMaterial, pk=pk, user=request.user)
    messages_list = ChatMessage.objects.filter(material=material).order_by('created_at')
    
    context = {
        'material': material,
        'messages': messages_list,
    }
    
    return render(request, 'chat/history.html', context)


# ============================================================================
# Study Session Tracking
# ============================================================================

@login_required(login_url='studyapp:login')
@require_http_methods(["POST"])
def start_session(request, pk):
    """Start a study session."""
    material = get_object_or_404(StudyMaterial, pk=pk, user=request.user)
    activity_type = request.POST.get('activity_type', 'reading')
    
    session = StudySession.objects.create(
        user=request.user,
        material=material,
        activity_type=activity_type,
    )
    
    request.session['current_session_id'] = session.id
    return JsonResponse({'session_id': session.id})


@login_required(login_url='studyapp:login')
@require_http_methods(["POST"])
def end_session(request):
    """End the current study session."""
    session_id = request.session.get('current_session_id')
    
    if session_id:
        try:
            session = StudySession.objects.get(id=session_id)
            session.end_time = timezone.now()
            session.save()
            del request.session['current_session_id']
            return JsonResponse({'success': True})
        except StudySession.DoesNotExist:
            pass
    
    return JsonResponse({'success': False})


@login_required(login_url='studyapp:login')
def study_stats(request):
    """View user's study statistics."""
    user = request.user
    
    sessions = StudySession.objects.filter(user=user, end_time__isnull=False)
    total_minutes = sum(s.duration_minutes for s in sessions)
    
    activity_breakdown = StudySession.objects.filter(user=user).values('activity_type').annotate(
        count=Count('id')
    )
    
    materials_count = StudyMaterial.objects.filter(user=user).count()
    summaries_count = Summary.objects.filter(material__user=user).count()
    questions_count = PracticeQuestion.objects.filter(material__user=user).count()
    
    context = {
        'total_sessions': sessions.count(),
        'total_study_minutes': total_minutes,
        'activity_breakdown': activity_breakdown,
        'materials_count': materials_count,
        'summaries_count': summaries_count,
        'questions_count': questions_count,
    }
    
    return render(request, 'stats.html', context)


# ============================================================================
# API Endpoints (for AJAX)
# ============================================================================

@login_required(login_url='studyapp:login')
def api_material_summary(request, pk):
    """API endpoint to get material summary."""
    material = get_object_or_404(StudyMaterial, pk=pk, user=request.user)
    summary = Summary.objects.filter(material=material).first()
    
    if summary:
        return JsonResponse({
            'exists': True,
            'summary': summary.summary_text,
            'key_points': summary.key_points,
        })
    return JsonResponse({'exists': False})


from django.db import models
