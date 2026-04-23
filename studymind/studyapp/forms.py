"""
Forms for the study app.
"""
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import StudyMaterial, ChatMessage


class UserRegistrationForm(UserCreationForm):
    """Form for user registration."""
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].help_text = 'At least 8 characters'
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})


class StudyMaterialForm(forms.ModelForm):
    """Form for creating/updating study materials."""
    class Meta:
        model = StudyMaterial
        fields = ['title', 'description', 'content', 'material_type', 'file']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter material title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Optional description'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 10, 'placeholder': 'Paste or type your study notes here...'}),
            'material_type': forms.Select(attrs={'class': 'form-control'}),
            'file': forms.FileInput(attrs={'class': 'form-control'}),
        }


class ChatForm(forms.Form):
    """Form for user messages in chat."""
    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Ask a question about your study material...',
            'maxlength': 2000,
        }),
        max_length=2000,
        label='Your Question'
    )
