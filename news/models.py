from django.db import models
from django.template.defaultfilters import slugify
from django.utils import timezone

from unidecode import unidecode


class Post(models.Model):
    post_title = models.CharField(verbose_name="Заголовок", max_length=100)
    post_short_description = models.CharField(verbose_name="Краткое описание", max_length=100, blank=True)
    post_full_description = models.TextField(verbose_name="Описание", max_length=5000)
    post_author = models.CharField(verbose_name="Автор", max_length=20)
    post_publication_date = models.DateTimeField(verbose_name="Дата публикации", default=timezone.now)
    post_slug = models.SlugField(default="", unique=True, editable=False, max_length=100)
    post_is_active = models.BooleanField(verbose_name="Активно", default=True)

    class Meta:
        verbose_name = "Пост"
        verbose_name_plural = "Посты"

    def save(self, *args, **kwargs):
        self.post_slug = slugify(unidecode(self.post_title))
        super(Post, self).save()

    def __str__(self):
        return self.post_title
