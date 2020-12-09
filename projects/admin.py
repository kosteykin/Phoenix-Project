from django import forms
from django.contrib import admin
from .models import Project, Tasks, News

admin.site.register(News)


class TasksAdminForm(forms.ModelForm):
    class Meta:
        model = Tasks
        fields = '__all__'


class TasksAdmin(admin.ModelAdmin):
    form = TasksAdminForm

    list_display = (
        "tasks_title", "tasks_project_id", "tasks_tracker", "tasks_status", "tasks_priority", "tasks_start_date",
        "tasks_complete_date",
        "tasks_time_evaluation", "tasks_prepared")
    list_filter = ("tasks_tracker", "tasks_status", "tasks_start_date", "tasks_prepared")
    search_fields = (
        "tasks_project_id__project_name", "tasks_title", "tasks_tracker", "tasks_status", "tasks_priority",
        "tasks_time_evaluation", "tasks_prepared")


admin.site.register(Tasks, TasksAdmin)


class ProjectAdminForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = '__all__'


# class TasksInLine(admin.TabularInline):
#  model = Tasks
#  extra = 0
# fk_name = "tasks_project_id"


class ProjectAdmin(admin.ModelAdmin):
    form = ProjectAdminForm

    list_display = ("project_name", "project_publication_date", "project_author")
    list_filter = ("project_publication_date", "project_author")
    search_fields = ("project_name", "project_author")


# inlines = [TasksInLine]


admin.site.register(Project, ProjectAdmin)
