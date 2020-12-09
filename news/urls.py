from django.urls import path

from . import views

app_name = "news"
urlpatterns = [
    path('', views.newsindex),
    path('<int:id>/<slug:post_slug>/', views.news_post_detail_view, name='post_detail'),
]
