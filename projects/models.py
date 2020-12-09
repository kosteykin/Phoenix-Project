from django.db import models
from django.template.defaultfilters import slugify
from django.utils import timezone

from unidecode import unidecode
#123

class Project(models.Model):
    project_name = models.CharField(verbose_name="Название проекта", max_length=50)
    project_short_description = models.CharField(verbose_name="Краткое описание", max_length=100)
    project_full_description = models.CharField(verbose_name="Полное описание", max_length=5000)
    project_publication_date = models.DateTimeField(verbose_name="Дата публикации", auto_now_add=True)
    project_author = models.CharField(verbose_name="Автор", max_length=15)
    project_slug = models.SlugField(default="", unique=True, editable=False)

    class Meta:
        verbose_name = "Проект"
        verbose_name_plural = "Проекты"

    def save(self, *args, **kwargs):
        self.project_publication_date = timezone.now()
        self.project_slug = slugify(unidecode(self.project_name))
        super(Project, self).save()

    def __str__(self):
        return self.project_name


class Tasks(models.Model):
    tracker_choices = ("Bug", "Bug"), ("Feature", "Feature"), ("Support", "Support")
    priority_choices = ("Low", "Low"), ("Normal", "Normal"), ("High", "High"), ("Urgent", "Urgent"), (
        "Immediate", "Immediate")
    prepared_choices = [(str(i), str(i) + "%") for i in range(0, 110, 10)]  # 0-100%
    status_choices = ("New", "New"), ("In Progress", "In Progress"), ("Closed", "Closed")

    tasks_project_id = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name="Проект", null=True, blank=True)
    tasks_tracker = models.CharField(verbose_name="Трекер", choices=tracker_choices, default="Bug", max_length=50)
    tasks_title = models.CharField(verbose_name="Тема", max_length=100)
    tasks_description = models.TextField(verbose_name="Описание", max_length=5000, blank=True)
    tasks_status = models.CharField(verbose_name="Статус", choices=status_choices, default="New", max_length=50)
    tasks_priority = models.CharField(verbose_name="Приоритет", choices=priority_choices, default="Normal",
                                      max_length=50)
    tasks_assigned = models.CharField(verbose_name="Назначена", max_length=50, blank=True)
    tasks_category = models.CharField(verbose_name="Категория", default="", max_length=50, blank=True)
    tasks_files = models.FileField(verbose_name="Файлы", upload_to="uploads/", blank=True)
    tasks_start_date = models.DateField(verbose_name="Начало выполнения")
    tasks_complete_date = models.DateField(verbose_name="Дата выполнения", null=True, blank=True)
    tasks_time_evaluation = models.IntegerField(verbose_name="Кол-во часов", default=0, blank=True)
    tasks_prepared = models.CharField(verbose_name="Готовность", choices=prepared_choices, default=0, max_length=50,
                                      blank=True)

    class Meta:
        verbose_name = "Задача"
        verbose_name_plural = "Задачи"

    def save(self, *args, **kwargs):
        super(Tasks, self).save()

    def __str__(self):
        return self.tasks_title

    def __unicode__(self):
        return self.tasks_project_id


class News(models.Model):
    news_project_id = models.ForeignKey(Project, on_delete=models.CASCADE)
    news_title = models.CharField(verbose_name="Заголовок", max_length=50)
    news_summary = models.CharField(verbose_name="Краткое описание", max_length=100)
    news_description = models.CharField(verbose_name="Описание", max_length=1000)
    news_author = models.CharField(verbose_name="Автор", max_length=20)
    news_created_on = models.DateField(verbose_name="Дата публикации")
    news_project_slug = models.SlugField(default="", unique=True, editable=False)

    def save(self, *args, **kwargs):
        self.news_project_slug = slugify(unidecode(self.news_title))
        super(News, self).save()

    def __str__(self):
        return self.news_title
