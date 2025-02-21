from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm 
from django.contrib.auth.models import User


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = [
            "name",
            "description",
            "progress",
            "start_date",
            "deadline",
            "logo",
            "status",
        ]
        widgets = {
            # range form for the progress with class form-range
            "progress": forms.NumberInput(attrs={"class": "form-range"}),
            "start_date": forms.DateInput(attrs={"type": "date"}),
            "deadline": forms.DateInput(attrs={"type": "date"}),
            "description": forms.Textarea(attrs={"rows": 4}),
        }


class MaterialForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = ["name", "description", "status", "published"]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4}),
        }


class MaterialRequestForm(forms.ModelForm):
    class Meta:
        model = MaterialRequest
        fields = ["quantity", "from_date", "to_date"]
        widgets = {
            "from_date": forms.DateInput(attrs={"type": "date"}),
            "to_date": forms.DateInput(attrs={"type": "date"}),
        }


class FacultyForm(forms.ModelForm):
    class Meta:
        model = Faculty
        fields = ["arabic_name", "latin_name", "abreviated_name"]


class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ["arabic_name", "latin_name", "abreviated_name"]


class SpecialityForm(forms.ModelForm):
    class Meta:
        model = Speciality
        fields = ["arabic_name", "latin_name", "abreviated_name"]


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()  # Add email field
    
    class Meta:
        model = User
        fields = ['username', 'email']

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User 
        fields = ['username', 'email']

class TeamMemberForm(forms.ModelForm):
    class Meta:
        model = TeamMember
        fields = [
            
            "photo",
            "phone",
            "bio",
            "role",
            "gender",
            "faculty",
            "department",
            "speciality",
        ]
        widgets = {
            "bio": forms.Textarea(attrs={"rows": 4}),
        }


class ProjectImageForm(forms.ModelForm):
    class Meta:
        model = ProjectImage
        fields = ["project", "image"]


class MaterialImageForm(forms.ModelForm):
    class Meta:
        model = MaterialImage
        fields = ["material", "image"]


class ProjectFileForm(forms.ModelForm):
    class Meta:
        model = ProjectFile
        fields = ["project", "file"]


class MaterialFileForm(forms.ModelForm):
    class Meta:
        model = MaterialFile
        fields = ["material", "file"]


# Additional specialized forms


class ProjectUpdateForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ["progress", "status"]
        widgets = {
            "progress": forms.Select(attrs={"class": "form-range"}),
            "status": forms.Select(attrs={"class": "form-control"}),
        }


class TeamMemberUpdateForm(forms.ModelForm):
    class Meta:
        model = TeamMember
        fields = ["phone", "bio", "photo"]
        widgets = {
            "bio": forms.Textarea(attrs={"rows": 4}),
        }


class MaterialSearchForm(forms.Form):
    search_query = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "Search materials..."}),
    )
    status = forms.ChoiceField(
        choices=[("", "All")] + Material.STATUS_CHOICES, required=False
    )


class ProjectSearchForm(forms.Form):
    search_query = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "Search projects..."}),
    )
    status = forms.ChoiceField(
        choices=[("", "All")] + Project.STATUS_CHOICES, required=False
    )
    date_from = forms.DateField(
        required=False, widget=forms.DateInput(attrs={"type": "date"})
    )
    date_to = forms.DateField(
        required=False, widget=forms.DateInput(attrs={"type": "date"})
    )


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result


class MultipleFileUploadForm(forms.Form):
    files = MultipleFileField(required=False)


class MultipleImageUploadForm(forms.Form):
    images = MultipleFileField(required=False)


class MaterialRequestSearchForm(forms.Form):
    search_query = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "Search requests..."}),
    )
    date_from = forms.DateField(
        required=False, widget=forms.DateInput(attrs={"type": "date"})
    )
    date_to = forms.DateField(
        required=False, widget=forms.DateInput(attrs={"type": "date"})
    )


class PlanForm(forms.ModelForm):
    class Meta:
        model = Plan
        fields = ["project"]


class PhaseForm(forms.ModelForm):
    class Meta:
        model = Phase
        fields = ["plan", "title", "deadline"]
        widgets = {
            "deadline": forms.DateInput(attrs={"type": "date"}),
        }


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["name", "description", "phase"]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4}),
        }


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ["name", "date", "description", "task"]
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
            "description": forms.Textarea(attrs={"rows": 4}),
        }


class ActionUpdatesForm(forms.ModelForm):
    class Meta:
        model = ActionUpdates
        fields = ["action", "done_time"]
        widgets = {
            "done_time": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }


class PhaseSearchForm(forms.Form):
    search_query = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "Search phases..."}),
    )
    deadline_from = forms.DateField(
        required=False, widget=forms.DateInput(attrs={"type": "date"})
    )
    deadline_to = forms.DateField(
        required=False, widget=forms.DateInput(attrs={"type": "date"})
    )


class TaskSearchForm(forms.Form):
    search_query = forms.CharField(
        required=False, widget=forms.TextInput(attrs={"placeholder": "Search tasks..."})
    )
    phase = forms.ModelChoiceField(
        queryset=Phase.objects.all(), required=False, empty_label="All Phases"
    )


class EventSearchForm(forms.Form):
    search_query = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "Search events..."}),
    )
    date_from = forms.DateField(
        required=False, widget=forms.DateInput(attrs={"type": "date"})
    )
    date_to = forms.DateField(
        required=False, widget=forms.DateInput(attrs={"type": "date"})
    )
    task = forms.ModelChoiceField(
        queryset=Task.objects.all(), required=False, empty_label="All Tasks"
    )
