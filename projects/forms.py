from django import forms
from projects.models import Tasks, Project


class TaskAddForm(forms.ModelForm):
    class Meta:
        model = Tasks
        fields = ['tasks_project_id', 'tasks_tracker', 'tasks_title', 'tasks_description', 'tasks_status',
                  'tasks_priority', 'tasks_start_date']


class ProjectAddForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['project_name', 'project_short_description', 'project_full_description', 'project_author']


class TaskEditForm(forms.ModelForm):
    class Meta:
        model = Tasks
        fields = '__all__'