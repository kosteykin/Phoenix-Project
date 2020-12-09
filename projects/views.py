from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from projects.models import Project, Tasks, News
from projects.forms import TaskAddForm, ProjectAddForm, TaskEditForm


def project_index(request):  # Список проектов
    project_list = Project.objects.order_by("-project_publication_date").all()
    project_count = len(project_list)  # Количество проектов
    paginator = Paginator(project_list, 10)  # max: 10
    page = request.GET.get("page")
    try:
        project_list = paginator.page(page)
    except PageNotAnInteger:
        project_list = paginator.page(1)
    except EmptyPage:
        project_list = paginator.page(paginator.num_pages)
    context = {
        "project_list": project_list,
        "project_count": project_count,  # Количество проектов
    }
    return render(request, template_name="projects/index.html", context=context)


def project_detail_view(request, project_slug, id):
    project = get_object_or_404(Project, pk=id)
    project_name = Project.objects.get(id=id).project_name  # Вывод имени текущего проекта

    try:
        news_project_list = News.objects.all().filter(news_project_id=id)  # Список новостей для текущего проекта
        news_count_list = len(news_project_list)
    except News.DoesNotExist:
        news_project_list = "Нет новостей"

    try:
        tasks_project_list = Tasks.objects.all().filter(tasks_project_id=id)  # Список задач для текущего проекта
        countlist = len(tasks_project_list)  # Счетчик задач для текущего проекта
        bug_list = len(Tasks.objects.filter(tasks_tracker__contains="Bug",
                                            tasks_project_id=id))  # Количество "Bug" в задачах для текущего проекта
        feature_list = len(Tasks.objects.filter(tasks_tracker__contains="Feature",
                                                tasks_project_id=id))  # Количество "Feature" в задачах для текущего проекта
        support_list = len(Tasks.objects.filter(tasks_tracker__contains="Support",
                                                tasks_project_id=id))  # Количество "Support" в задачах для текущего проекта
    except Tasks.DoesNotExist:
        tasks_project_list = "Задач нет"

    context = {
        "project": project,
        "project_name": project_name,  # Вывод имени текущего проекта
        "news_project_list": news_project_list,  # Список новостей для текущего проекта
        "tasks_project_list": tasks_project_list,  # Список задач для текущего проекта
        "countlist": countlist,  # Счетчик задач для текущего проекта
        "bug_list": bug_list,  # Количество "Bug" в задачах для текущего проекта
        "feature_list": feature_list,  # Количество "Feature" в задачах для текущего проекта
        "support_list": support_list,  # Количество "Support" в задачах для текущего проекта
        "news_count_list": news_count_list,
    }
    return render(request, template_name="projects/detail.html", context=context)


def project_news_detail_view(request, id):
    news = get_object_or_404(News, pk=id)
    context = {
        "news": news,
    }
    return render(request, template_name="projects/project_news_detail.html", context=context)


def project_tasks_view(request, id):  # Вывод количества задач для текущего проекта
    project = get_object_or_404(Project, pk=id)
    project_name = Project.objects.get(id=id).project_name
    tasks_list = Tasks.objects.all().filter(tasks_project_id=id)
    context = {
        "project_name": project_name,
        "tasks_list": tasks_list,
    }
    return render(request, template_name="projects/project_tasks_view.html", context=context)


def task_list_show(request):  # Вывод всех задач в базе на странице >>>http://phoenixfk.ru
    task_list = Tasks.objects.order_by("id").reverse().all()
    task_count = len(task_list)  # Счетчик количества задач
    paginator = Paginator(task_list, 10)  # max: 10
    page = request.GET.get("page")
    try:
        task_list = paginator.page(page)
    except PageNotAnInteger:
        task_list = paginator.page(1)
    except EmptyPage:
        task_list = paginator.page(paginator.num_pages)
    context = {
        "task_list": task_list,
        "task_count": task_count,
    }
    return render(request, "projects/tasks_list.html", context=context)


@login_required
def task_add(request):
    get_project_list = Project.objects.order_by("project_name")
    if request.method == 'POST':
        form = TaskAddForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.tasks_assigned = request.user
            form.save()
            return redirect("tasklist")
    else:
        form = TaskAddForm()
    return render(request, "projects/tasks_add.html", {"form": form, "get_project_list": get_project_list})


@login_required
def project_add(request):
    if request.method == 'POST':
        form = ProjectAddForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.project_author = request.user
            project.project_publication_date = timezone.now()
            form.save()
            return redirect("project:projects_list")
    else:
        form = ProjectAddForm()
    return render(request, "projects/project_add.html", {"form": form})


def tasks_task_view(request, id):  # Вывод количества задач для текущего проекта
    task = get_object_or_404(Tasks, pk=id)
    task_name = Tasks.objects.get(id=id).tasks_title
    context = {
        "task": task,
        "task_name": task_name,
    }
    return render(request, template_name="projects/tasks_view_task.html", context=context)


@login_required
def tasks_task_edit(request, id):
    task = get_object_or_404(Tasks, pk=id)
    form = TaskEditForm(request.POST, instance=task)
    if request.method == 'POST':
        if form.is_valid():
            task = form.save(commit=False)
            form.save()
            return redirect("tasklist")
    else:
        form = TaskEditForm()
    return render(request, "projects/tasks_edit.html",
                  {"form": form,
                   "task": task,
                   })


# AUTH

def logout_view(request):
    logout(request)
    return redirect('/')


def auth_login(request):
    return redirect('/')


def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, "register.html", {"form": form})
