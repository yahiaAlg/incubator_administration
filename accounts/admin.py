from django.contrib import admin
from .models import *


class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 1


class ProjectFileInline(admin.TabularInline):
    model = ProjectFile
    extra = 1


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("name", "progress", "start_date", "deadline", "status")
    list_filter = ("status", "start_date", "deadline")
    search_fields = ("name", "description")
    inlines = [ProjectImageInline, ProjectFileInline]
    date_hierarchy = "start_date"


class MaterialImageInline(admin.TabularInline):
    model = MaterialImage
    extra = 1


class MaterialFileInline(admin.TabularInline):
    model = MaterialFile
    extra = 1


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ("name", "status", "published")
    list_filter = ("status", "published")
    search_fields = ("name", "description")
    inlines = [MaterialImageInline, MaterialFileInline]


@admin.register(MaterialRequest)
class MaterialRequestAdmin(admin.ModelAdmin):
    list_display = (
        "material",
        "project",
        "quantity",
        "acquired_date",
        "from_date",
        "to_date",
    )
    list_filter = ("acquired_date", "from_date", "to_date")
    search_fields = ("material__name", "project__name")
    date_hierarchy = "acquired_date"


@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    list_display = ("arabic_name", "latin_name", "abreviated_name")
    search_fields = ("arabic_name", "latin_name", "abreviated_name")


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ("arabic_name", "latin_name", "abreviated_name")
    search_fields = ("arabic_name", "latin_name", "abreviated_name")


@admin.register(Speciality)
class SpecialityAdmin(admin.ModelAdmin):
    list_display = ("arabic_name", "latin_name", "abreviated_name")
    search_fields = ("arabic_name", "latin_name", "abreviated_name")


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "project",
        "role",
        "is_project_leader",
        "faculty",
        "department",
    )
    list_filter = ("role", "gender", "is_project_leader", "is_permitted_to_demand")
    search_fields = ("user__username", "user__first_name", "user__last_name", "phone")
    raw_id_fields = ("user", "project", "faculty", "department", "speciality")


class PhaseInline(admin.TabularInline):
    model = Phase
    extra = 1


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ("project", "get_phase_count")
    search_fields = ("project__name",)
    inlines = [PhaseInline]

    def get_phase_count(self, obj):
        return obj.phases.count()

    get_phase_count.short_description = "Number of Phases"


class TaskInline(admin.TabularInline):
    model = Task
    extra = 1


@admin.register(Phase)
class PhaseAdmin(admin.ModelAdmin):
    list_display = ("title", "plan", "deadline", "get_task_count")
    list_filter = ("deadline",)
    search_fields = ("title", "plan__project__name")
    date_hierarchy = "deadline"
    inlines = [TaskInline]

    def get_task_count(self, obj):
        return obj.tasks.count()

    get_task_count.short_description = "Number of Tasks"


class EventInline(admin.TabularInline):
    model = Event
    extra = 1


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("name", "phase", "get_event_count")
    search_fields = ("name", "description", "phase__title")
    list_filter = ("phase__plan__project",)
    inlines = [EventInline]

    def get_event_count(self, obj):
        return obj.events.count()

    get_event_count.short_description = "Number of Events"


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("name", "date", "task")
    list_filter = ("date",)
    search_fields = ("name", "description", "task__name")
    date_hierarchy = "date"


@admin.register(ActionUpdates)
class ActionUpdatesAdmin(admin.ModelAdmin):
    list_display = ("action", "done_time")
    list_filter = ("done_time",)
    search_fields = ("action",)
    date_hierarchy = "done_time"


# Register the remaining models for basic admin interface
admin.site.register(ProjectImage)
admin.site.register(MaterialImage)
admin.site.register(ProjectFile)
admin.site.register(MaterialFile)
