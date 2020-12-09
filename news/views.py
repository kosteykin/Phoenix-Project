from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Post


def newsindex(request):
    post_list = Post.objects.order_by("-post_publication_date").all()
    paginator = Paginator(post_list, 10)
    page = request.GET.get("page")
    try:
        post_list = paginator.page(page)
    except PageNotAnInteger:
        post_list = paginator.page(1)
    except EmptyPage:
        post_list = paginator.page(paginator.num_pages)
    context = {
        "post_list": post_list,
    }
    return render(request, "news/index.html", context=context)


def news_post_detail_view(request, post_slug, id):
    post = get_object_or_404(Post, pk=id)
    context = {
        "post": post,
    }
    return render(request, template_name="news/post_detail_view.html", context=context)
