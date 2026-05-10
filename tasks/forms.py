from django import forms
from django.conf import settings
from django.contrib.auth import get_user_model

from .models import Task
from projects.models import Membership, Project

User = get_user_model()


class TaskForm(forms.ModelForm):
    """
    Task creation form. Filters:
    - project: only projects the user is an ADMIN of (only admins can create tasks)
    - assignee: only members of the selected project (handled client-side via AJAX or
      broadly to all users in the project's membership; defaults to all users for simplicity)
    """

    class Meta:
        model = Task
        fields = ['title', 'description', 'project', 'assignee', 'priority', 'due_date']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)

        if user:
            admin_project_ids = Membership.objects.filter(
                user=user, role=Membership.ADMIN
            ).values_list('project_id', flat=True)
            self.fields['project'].queryset = Project.objects.filter(id__in=admin_project_ids)

        project_id = None
        if 'project' in self.initial:
            project_id = self.initial['project']
        elif self.data.get('project'):
            project_id = self.data.get('project')
        elif self.instance and self.instance.pk and self.instance.project:
            project_id = self.instance.project.id

        if project_id:
            member_user_ids = Membership.objects.filter(
                project_id=project_id
            ).values_list('user_id', flat=True)
            self.fields['assignee'].queryset = User.objects.filter(id__in=member_user_ids)
        else:
            self.fields['assignee'].queryset = User.objects.none()

        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
        self.fields['project'].widget.attrs.update({'class': 'form-select', 'id': 'id_project'})
        self.fields['assignee'].widget.attrs.update({'class': 'form-select', 'id': 'id_assignee'})
        self.fields['priority'].widget.attrs.update({'class': 'form-select'})
        self.fields['assignee'].required = False
        self.fields['description'].required = False


class TaskUpdateForm(forms.ModelForm):
    """
    Task update form (status/priority/assignee).
    Assignee is filtered to project members only.
    """

    class Meta:
        model = Task
        fields = ['title', 'description', 'assignee', 'status', 'priority', 'due_date']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, project=None, **kwargs):
        super().__init__(*args, **kwargs)

        if project:
            member_user_ids = Membership.objects.filter(
                project=project
            ).values_list('user_id', flat=True)
            self.fields['assignee'].queryset = User.objects.filter(id__in=member_user_ids)

        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
        self.fields['assignee'].widget.attrs.update({'class': 'form-select'})
        self.fields['priority'].widget.attrs.update({'class': 'form-select'})
        self.fields['assignee'].required = False
        self.fields['description'].required = False


class TaskStatusUpdateForm(forms.ModelForm):
    """
    Form for members to update only the status of their assigned tasks.
    """
    class Meta:
        model = Task
        fields = ['status']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['status'].widget.attrs.update({'class': 'form-select'})
        
        all_choices = Task.STATUS_CHOICES
        self.fields['status'].choices = [c for c in all_choices if c[0] != Task.COMPLETED]