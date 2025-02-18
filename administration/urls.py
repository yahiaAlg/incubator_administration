from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("export/projects/csv/", views.export_projects_csv, name="export_projects_csv"),
    # ... other URLs ...
    path("projects/create/", views.project_create, name="project_create"),
    path("projects/<int:pk>/update/", views.project_update, name="project_update"),
    path("projects/<int:pk>/delete/", views.project_delete, name="project_delete"),
    path("projects/<int:pk>/data/", views.get_project_data, name="get_project_data"),
    path(
        "projects/<int:pk>/detail/",
        views.ProjectDetailView.as_view(),
        name="project_detail",
    ),
]
