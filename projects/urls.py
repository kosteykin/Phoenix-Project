from django.urls import path

from . import views

app_name = "project"
urlpatterns = [
    path('', views.project_index, name='projects_list'),
    path('add/', views.project_add, name='project_add'),
    path('<int:id>/<slug:project_slug>/', views.project_detail_view, name='detail'),
    path('news/<int:id>/', views.project_news_detail_view, name='project_news_detail'),
    path('tasks/<int:id>/', views.project_tasks_view, name='project_tasks_view'),
    path('tasks/<int:id>/view/', views.tasks_task_view, name='task_view'),
    path('tasks/<int:id>/edit/', views.tasks_task_edit, name='task_edit'),
]
