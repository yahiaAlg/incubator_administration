#!/bin/bash

# Create virtual environment
echo "Creating virtual environment..."
python -m venv venv
source venv/bin/activate

# Install required packages
echo "Installing required packages..."
pip install django
pip install pillow

# Create Django project
echo "Creating Django project..."
django-admin startproject project_management .

# Create apps
echo "Creating Django apps..."
python manage.py startapp accounts
python manage.py startapp administration

# Create directory structure
echo "Creating directory structure..."
mkdir -p accounts/templates/accounts
mkdir -p administration/templates/administration
mkdir -p media/profile_pics
mkdir -p media/project_images

# Create accounts app files
echo "Creating accounts app files..."

# accounts/models.py
cat > accounts/models.py << 'EOL'
from django.db import models
from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=20, blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True)
    department = models.CharField(max_length=100, blank=True)
    position = models.CharField(max_length=100, blank=True)
    location = models.CharField(max_length=100, blank=True)
    timezone = models.CharField(max_length=50, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class ProjectMember(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='project_member')
    project = models.ForeignKey('administration.Project', on_delete=models.CASCADE, related_name='members')
    join_date = models.DateField(auto_now_add=True)
    skills = models.TextField(blank=True)
    role = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username} - {self.project.name}"

class ProjectLeader(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='project_leader')
    projects = models.ManyToManyField('administration.Project', related_name='leaders')
    date_assigned = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return f"Leader: {self.user.username}"
EOL

# accounts/forms.py
cat > accounts/forms.py << 'EOL'
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Profile, ProjectMember

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Email address',
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Password',
    }))

class ProfileUpdateForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(max_length=254, required=True)

    class Meta:
        model = Profile
        fields = ['phone', 'bio', 'department', 'position', 'location', 
                 'timezone', 'profile_picture']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.user:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
            self.fields['email'].initial = self.instance.user.email

    def save(self, commit=True):
        profile = super().save(commit=False)
        if commit:
            user = profile.user
            user.first_name = self.cleaned_data['first_name']
            user.last_name = self.cleaned_data['last_name']
            user.email = self.cleaned_data['email']
            user.save()
            profile.save()
        return profile

class ProjectMemberForm(forms.ModelForm):
    class Meta:
        model = ProjectMember
        fields = ['skills', 'role']
        widgets = {
            'skills': forms.Textarea(attrs={'rows': 3}),
        }

class ChangePasswordForm(forms.Form):
    current_password = forms.CharField(widget=forms.PasswordInput)
    new_password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')

        if new_password and confirm_password and new_password != confirm_password:
            raise forms.ValidationError("New passwords don't match")
        return cleaned_data
EOL

# accounts/views.py
cat > accounts/views.py << 'EOL'
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse
from .forms import (
    CustomAuthenticationForm, ProfileUpdateForm, 
    ProjectMemberForm, ChangePasswordForm
)
from .models import Profile, ProjectMember, ProjectLeader
from administration.models import Project

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
        
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                if hasattr(user, 'project_leader'):
                    return redirect('dashboard')
                else:
                    messages.error(request, "You don't have permission to access the dashboard.")
                    logout(request)
                    return redirect('login')
        else:
            messages.error(request, "Invalid email or password.")
    else:
        form = CustomAuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard(request):
    if not hasattr(request.user, 'project_leader'):
        raise PermissionDenied
    
    leader = request.user.project_leader
    context = {
        'projects': leader.projects.all(),
    }
    return render(request, 'accounts/project_leader_dashboard.html', context)

@login_required
def profile_update(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')
            return redirect('dashboard')
    else:
        form = ProfileUpdateForm(instance=request.user.profile)
    
    return render(request, 'accounts/project_leader_dashboard.html', {'form': form})

@login_required
def change_password(request):
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            if request.user.check_password(form.cleaned_data['current_password']):
                request.user.set_password(form.cleaned_data['new_password'])
                request.user.save()
                messages.success(request, 'Password changed successfully')
                return redirect('login')
            else:
                messages.error(request, 'Current password is incorrect')
    else:
        form = ChangePasswordForm()
    
    return render(request, 'accounts/project_leader_dashboard.html', {'form': form})

@login_required
def project_members(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    if not project.leaders.filter(user=request.user).exists():
        raise PermissionDenied
    
    members = ProjectMember.objects.filter(project=project)
    return render(request, 'accounts/project_leader_dashboard.html', {
        'project': project,
        'members': members
    })

@login_required
def add_project_member(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    if not project.leaders.filter(user=request.user).exists():
        raise PermissionDenied
    
    if request.method == 'POST':
        form = ProjectMemberForm(request.POST)
        if form.is_valid():
            member = form.save(commit=False)
            member.project = project
            member.save()
            messages.success(request, 'Member added successfully')
            return redirect('project_members', project_id=project_id)
    else:
        form = ProjectMemberForm()
    
    return render(request, 'accounts/project_leader_dashboard.html', {
        'form': form,
        'project': project
    })

@login_required
def remove_project_member(request, member_id):
    member = get_object_or_404(ProjectMember, id=member_id)
    if not member.project.leaders.filter(user=request.user).exists():
        raise PermissionDenied
    
    member.delete()
    messages.success(request, 'Member removed successfully')
    return redirect('project_members', project_id=member.project.id)

@login_required
def update_project_member(request, member_id):
    member = get_object_or_404(ProjectMember, id=member_id)
    if not member.project.leaders.filter(user=request.user).exists():
        raise PermissionDenied
    
    if request.method == 'POST':
        form = ProjectMemberForm(request.POST, instance=member)
        if form.is_valid():
            form.save()
            messages.success(request, 'Member information updated successfully')
            return redirect('project_members', project_id=member.project.id)
    else:
        form = ProjectMemberForm(instance=member)
    
    return render(request, 'accounts/project_leader_dashboard.html', {
        'form': form,
        'member': member
    })
EOL

# accounts/urls.py
cat > accounts/urls.py << 'EOL'
from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/update/', views.profile_update, name='profile_update'),
    path('profile/change-password/', views.change_password, name='change_password'),
    path('project/<int:project_id>/members/', views.project_members, name='project_members'),
    path('project/<int:project_id>/members/add/', views.add_project_member, name='add_project_member'),
    path('project/member/<int:member_id>/remove/', views.remove_project_member, name='remove_project_member'),
    path('project/member/<int:member_id>/update/', views.update_project_member, name='update_project_member'),
]
EOL

# Create template files
echo "Creating template files..."

# login.html
cat > accounts/templates/accounts/login.html << 'EOL'
{% extends 'base.html' %}

{% block content %}
<!-- Login template content will go here -->
{% endblock %}
EOL

# project_leader_dashboard.html
cat > accounts/templates/accounts/project_leader_dashboard.html << 'EOL'
{% extends 'base.html' %}

{% block content %}
<!-- Dashboard template content will go here -->
{% endblock %}
EOL

# Update project settings
echo "Updating project settings..."
cat > project_management/settings.py << 'EOL'
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'your-secret-key-here'

DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'accounts',
    'administration',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'project_management.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'project_management.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'dashboard'
LOGOUT_REDIRECT_URL = 'login'
EOL

# Update project URLs
cat > project_management/urls.py << 'EOL'
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),
    path('administration/', include('administration.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
EOL

# Create empty base.html template
mkdir -p templates
cat > templates/base.html << 'EOL'
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Project Management System</title>
</head>
<body>
    {% block content %}
    {% endblock %}
</body>
</html>
EOL

# Create static and media directories
mkdir -p static/css static/js static/img
mkdir -p media/profile_pics media/project_images

# Make migrations
echo "Making migrations..."
python manage.py makemigrations
python manage.py migrate

# Create superuser
echo "Creating superuser..."
echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'admin')" | python manage.py shell

echo "Project setup complete!"

# Make the script executable
chmod +x build.sh
EOL

Make the script executable and run it:
```bash
chmod +x build.sh
./build.sh