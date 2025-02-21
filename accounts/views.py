from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST
from .models import *
from .forms import *
from django.contrib.auth import logout


@login_required
def dashboard(request):
    try:
        team_member = TeamMember.objects.get(user=request.user)

        if team_member.project is None:
            # User has no project, redirect to create project page
            return redirect("create_project")

        context = {
            "team_member": team_member,
            "team_member_update_form": TeamMemberUpdateForm(instance=team_member),
            "project": team_member.project,
            "project_form": ProjectForm(instance=team_member.project),
            "project_images_form": ProjectImageForm(
                data={
                    "project": team_member.project,
                }
            ),
            "project_files_form": ProjectFileForm(
                data={"project": team_member.project},
            ),
            "material_request_form": MaterialRequestForm(),
            "available_materials": Material.objects.filter(status="available"),
            "material_requests": MaterialRequest.objects.filter(
                project=team_member.project
            ),
            "team_members": TeamMember.objects.filter(project=team_member.project),
            "team_member_form": TeamMemberForm(),
            "user_creation_form": UserRegistrationForm(),
            "user_update_form": UserUpdateForm(instance=team_member.user),
        }
        return render(request, "dashboard.html", context)

    except TeamMember.DoesNotExist:
        # If no TeamMember exists for the user, create one
        team_member = TeamMember.objects.create(
            user=request.user,
            is_permitted_to_demand=True,
            is_project_leader=True,
            phone="",
            bio="",
            role="supervisor",
            gender="male",
            photo="default_image_placeholder.png",
        )
        return redirect("create_project")


@login_required
def create_project(request):
    if request.method == "POST":
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save()

            # Associate the project with the team member
            team_member = request.user.team_member
            team_member.project = project
            team_member.is_project_leader = True
            team_member.save()

            messages.success(request, "Project created successfully.")
            return redirect("dashboard")
    else:
        form = ProjectForm()

    return render(request, "create_project.html", {"form": form})


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

    member_form = TeamMemberForm(request.POST, request.FILES)
    if member_form.is_valid():
        member = member_form.save(commit=False)
        member.project = request.user.team_member.project
        member.save()
        messages.success(request, "Team member added successfully.")
    else:
        messages.error(request, f"Error adding team member.{member_form.errors}")
    return redirect("dashboard")


@login_required
@require_POST
def update_team_member(request):
    member_id = int(request.POST.get("member_id", ""))
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
        reservation = form.save(commit=False)
        reservation.material = material
        reservation.project = request.user.team_member.project
        reservation.save()
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
