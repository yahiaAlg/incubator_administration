from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST
from .models import *
from .forms import *
from django.contrib.auth import logout


@login_required
def dashboard(request):
    team_member = get_object_or_404(TeamMember, user=request.user)
    context = {
        "team_member": team_member,
        "team_member_update_form": TeamMemberUpdateForm(instance=team_member),
        "project": team_member.project,
        "project_form": ProjectForm(instance=team_member.project),
        "available_materials": Material.objects.filter(status="available"),
        "material_requests": MaterialRequest.objects.filter(
            project=team_member.project
        ),
        "team_members": TeamMember.objects.filter(project=team_member.project),
        "team_member_form": TeamMemberForm(),
    }
    return render(request, "dashboard.html", context)


@login_required
@require_POST
def update_profile(request):
    team_member = get_object_or_404(TeamMember, user=request.user)
    form = TeamMemberUpdateForm(request.POST, request.FILES, instance=team_member)
    if form.is_valid():
        form.save()
        messages.success(request, "Profile updated successfully.")
    else:
        messages.error(request, "Error updating profile.")
    return redirect("dashboard")


@login_required
@require_POST
def add_team_member(request):
    if not request.user.team_member.is_project_leader:
        messages.error(request, "Only project leaders can add team members.")
        return redirect("dashboard")

    form = TeamMemberForm(request.POST, request.FILES)
    if form.is_valid():
        member = form.save(commit=False)
        member.project = request.user.team_member.project
        member.save()
        messages.success(request, "Team member added successfully.")
    else:
        messages.error(request, "Error adding team member.")
    return redirect("dashboard")


@login_required
@require_POST
def update_team_member(request, member_id):
    if not request.user.team_member.is_project_leader:
        messages.error(request, "Only project leaders can update team members.")
        return redirect("dashboard")

    member = get_object_or_404(TeamMember, id=member_id)
    form = TeamMemberForm(request.POST, request.FILES, instance=member)
    if form.is_valid():
        form.save()
        messages.success(request, "Team member updated successfully.")
    else:
        messages.error(request, "Error updating team member.")
    return redirect("dashboard")


@login_required
@require_POST
def update_project(request):
    project = request.user.team_member.project
    form = ProjectForm(request.POST, request.FILES, instance=project)
    if form.is_valid():
        form.save()

        # Handle multiple image uploads
        images = request.FILES.getlist("images")
        for image in images:
            ProjectImage.objects.create(project=project, image=image)

        # Handle multiple file uploads
        files = request.FILES.getlist("files")
        for file in files:
            ProjectFile.objects.create(project=project, file=file)

        messages.success(request, "Project updated successfully.")
    else:
        messages.error(request, "Error updating project.")
    return redirect("dashboard")


@login_required
@require_POST
def request_material(request, material_id):
    if not request.user.team_member.is_permitted_to_demand:
        messages.error(request, "You are not permitted to request materials.")
        return redirect("dashboard")

    material = get_object_or_404(Material, id=material_id)
    form = MaterialRequestForm(request.POST)
    if form.is_valid():
        request = form.save(commit=False)
        request.material = material
        request.project = request.user.team_member.project
        request.save()
        messages.success(request, "Material requested successfully.")
    else:
        messages.error(request, "Error requesting material.")
    return redirect("dashboard")


@login_required
@require_POST
def return_material(request, request_id):
    material_request = get_object_or_404(MaterialRequest, id=request_id)
    if material_request.project != request.user.team_member.project:
        messages.error(request, "You can only return materials for your project.")
        return redirect("dashboard")

    material_request.material.status = "available"
    material_request.material.save()
    material_request.delete()
    messages.success(request, "Material returned successfully.")
    return redirect("dashboard")


@login_required
@require_POST
def delete_project_image(request, image_id):
    image = get_object_or_404(ProjectImage, id=image_id)
    if image.project != request.user.team_member.project:
        messages.error(request, "You can only delete images from your project.")
        return redirect("dashboard")

    image.delete()
    messages.success(request, "Image deleted successfully.")
    return redirect("dashboard")


@login_required
@require_POST
def delete_project_file(request, file_id):
    file = get_object_or_404(ProjectFile, id=file_id)
    if file.project != request.user.team_member.project:
        messages.error(request, "You can only delete files from your project.")
        return redirect("dashboard")

    file.delete()
    messages.success(request, "File deleted successfully.")
    return redirect("dashboard")


@login_required
def logout_view(request):
    logout(request)
    return redirect("login")
