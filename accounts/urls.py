from django.urls import path
from . import views
from django.contrib.auth.views import LoginView

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("create-project/", views.create_project, name="create_project"),
    path("update-profile/", views.update_profile, name="update_profile"),
    path("add-team-member/", views.add_team_member, name="add_team_member"),
    path(
        "update-team-member/",
        views.update_team_member,
        name="update_team_member",
    ),
    path("update-project/", views.update_project, name="update_project"),
    path(
        "request-material/<int:material_id>/",
        views.request_material,
        name="request_material",
    ),
    path(
        "return-material/<int:request_id>/",
        views.return_material,
        name="return_material",
    ),
    path(
        "delete-project-image/<int:image_id>/",
        views.delete_project_image,
        name="delete_project_image",
    ),
    path(
        "delete-project-file/<int:file_id>/",
        views.delete_project_file,
        name="delete_project_file",
    ),
    path(
        "login/", LoginView.as_view(template_name="accounts/login.html"), name="login"
    ),
    path("logout/", views.logout_view, name="logout"),
]
