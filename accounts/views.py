from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from .forms import (
    CustomAuthenticationForm, ProfileUpdateForm, 
    ProjectMemberForm, ChangePasswordForm
)
from .models import ProjectMember
from administration.models import Project

from django.contrib.auth.models import User, Group

def check_user_in_group(user, group_names):
  """
  Checks if a user is in any of the specified groups.

  Args:
    user (User): The user object to check.
    group_names (list): A list of group names to check.

  Returns:
    bool: True if the user is in any of the groups, False otherwise.
  """
  # Get all group objects by name
  groups = Group.objects.filter(name__in=group_names)
  # Check if the user is in any of the groups
  return user.groups.filter(pk__in=groups).exists()



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


def dashboard(request):

    group_names = ["project_leader"]

    if check_user_in_group(request.user, group_names):
        messages.success(request,"User '{request.user.username}' is in one of the groups: {group_names}")
        return redirect(
            "login"
        )
    else:
        messages.error(request,f"User '{request.user.username}' is not in any of the groups: {group_names}")
        return render(request, 'accounts/project_leader_dashboard.html')
    

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
