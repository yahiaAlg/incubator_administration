# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from accounts.models import *
from django.views.decorators.http import require_http_methods

# detail template from generic template view
from django.views.generic import DetailView
from django.shortcuts import render
from django.db.models import Count, Q


@login_required
def home(request):
    # Get filter parameters from request
    status = request.GET.get("status")
    faculty = request.GET.get("faculty")
    team_leader = request.GET.get("team_leader")
    search_query = request.GET.get("search")

    # Start with all projects
    projects = Project.objects.select_related("team_leader").annotate(
        team_members_count=Count("team_member")
    )

    # Apply filters
    if status:
        projects = projects.filter(status=status)

    if faculty:
        projects = projects.filter(faculty=faculty)

    if team_leader:
        projects = projects.filter(team_leader_username_icontains=team_leader)

    if search_query:
        projects = projects.filter(
            Q(name__icontains=search_query)
            | Q(description__icontains=search_query)
            | Q(team_leader__full_name__icontains=search_query)
        )

    context = {
        "projects": projects,
    }

    return render(request, "pages/home.html", context)


def get_status_class(status):
    """Helper function to get Bootstrap class for status badges"""
    status_classes = {
        "active": "success",
        "on_hold": "warning",
        "completed": "secondary",
        "pending": "info",
        "cancelled": "danger",
    }
    return status_classes.get(status.lower(), "primary")


@login_required
def export_projects_csv(request):
    """Export projects data to CSV"""
    import csv
    from django.http import HttpResponse

    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="projects.csv"'

    writer = csv.writer(response)
    writer.writerow(
        [
            "Project Name",
            "Team Leader",
            "Start Date",
            "Deadline",
            "Status",
            "Progress",
            "Faculty",
            "Department",
        ]
    )

    projects = Project.objects.select_related("teamleader").all()

    for project in projects:
        writer.writerow(
            [
                project.name,
                project.teamleader.full_name if project.teamleader else "",
                project.start_date.strftime("%Y-%m-%d"),
                project.deadline.strftime("%Y-%m-%d"),
                project.status,
                f"{project.progress}%",
                project.faculty,
                project.department,
            ]
        )

    return response


@login_required
@require_http_methods(["POST"])
def project_create(request):
    try:
        # Extract data from request
        data = request.POST
        files = request.FILES

        # Create project
        project = Project.objects.create(
            name=data["name"],
            description=data["description"],
            start_date=data["start_date"],
            deadline=data["deadline"],
            faculty=data["faculty"],
            department=data["department"],
        )

        # Handle logo upload
        if "logo" in files:
            project.logo = files["logo"]
            project.save()

        # Set team leader
        if data.get("team_leader"):
            team_leader = TeamMember.objects.get(id=data["team_leader"])
            project.team_leader = team_leader
            project.save()

        messages.success(request, "Project created successfully")
        return redirect("home")

    except Exception as e:
        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return JsonResponse({"status": "error", "message": str(e)}, status=400)

        messages.error(request, f"Error creating project: {str(e)}")
        return redirect("home")


@login_required
@require_http_methods(["POST"])
def project_update(request, pk):
    try:
        project = get_object_or_404(Project, pk=pk)

        # Check permissions
        if not request.user.has_perm("change_project", project):
            raise PermissionDenied

        data = request.POST
        files = request.FILES

        # Update basic fields
        project.name = data["name"]
        project.description = data["description"]
        project.start_date = data["start_date"]
        project.deadline = data["deadline"]
        project.faculty = data["faculty"]
        project.department = data["department"]

        # Handle logo update
        if "logo" in files:
            project.logo = files["logo"]

        # Update team leader
        if data.get("team_leader"):
            team_leader = TeamMember.objects.get(id=data["team_leader"])
            project.team_leader = team_leader

        project.save()

        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return JsonResponse(
                {
                    "status": "success",
                    "message": "Project updated successfully",
                    "project": {
                        "id": project.id,
                        "name": project.name,
                        "status": project.status,
                        "start_date": project.start_date.strftime("%b %d, %Y"),
                    },
                }
            )

        messages.success(request, "Project updated successfully")
        return redirect("home")

    except Exception as e:
        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return JsonResponse({"status": "error", "message": str(e)}, status=400)

        messages.error(request, f"Error updating project: {str(e)}")
        return redirect("home")


@login_required
@require_http_methods(["POST"])
def project_delete(request, pk):
    try:
        project = get_object_or_404(Project, pk=pk)

        # Check permissions
        if not request.user.has_perm("delete_project", project):
            raise PermissionDenied

        project_name = project.name
        project.delete()

        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return JsonResponse(
                {
                    "status": "success",
                    "message": f'Project "{project_name}" deleted successfully',
                }
            )

        messages.success(request, f'Project "{project_name}" deleted successfully')
        return redirect("home")

    except Exception as e:
        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return JsonResponse({"status": "error", "message": str(e)}, status=400)

        messages.error(request, f"Error deleting project: {str(e)}")
        return redirect("home")


@login_required
def get_project_data(request, pk):
    """AJAX endpoint to get project data for edit modal"""
    try:
        project = get_object_or_404(Project, pk=pk)

        data = {
            "id": project.id,
            "name": project.name,
            "description": project.description,
            "start_date": project.start_date.strftime("%Y-%m-%d"),
            "deadline": project.deadline.strftime("%Y-%m-%d"),
            "faculty": project.faculty,
            "department": project.department,
            "team_leader": project.team_leader.id if project.team_leader else None,
            "logo_url": project.logo.url if project.logo else None,
        }

        return JsonResponse(data)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)


# a view to handle project detail pafge
class ProjectDetailView(DetailView):
    model = Project
    template_name = "pages/project_detail.html"
    context_object_name = "project"
