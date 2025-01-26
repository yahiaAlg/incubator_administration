from django.urls import path
from . import views

# import LoginView as view to make use of it from auth views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path(
        "",
        auth_views.LoginView.as_view(template_name="accounts/login.html"),
        name="login",
    ),
    path(
        "logout/",
        auth_views.LogoutView.as_view(template_name="accounts/logout.html"),
        name="logout",
    ),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("profile/update/", views.profile_update, name="profile_update"),
    path("profile/change-password/", views.change_password, name="change_password"),
    path(
        "project/<int:project_id>/members/",
        views.project_members,
        name="project_members",
    ),
    path(
        "project/<int:project_id>/members/add/",
        views.add_project_member,
        name="add_project_member",
    ),
    path(
        "project/member/<int:member_id>/remove/",
        views.remove_project_member,
        name="remove_project_member",
    ),
    path(
        "project/member/<int:member_id>/update/",
        views.update_project_member,
        name="update_project_member",
    ),
]
