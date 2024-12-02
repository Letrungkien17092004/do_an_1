from django.shortcuts import render
from django.views.decorators.http import require_GET
from ..models import Post
from django.core.paginator import Paginator

@require_GET
def index(request):
    return render(request, "home.html", {})

@require_GET
def chat_page(request):
    return render(request, "chat-page.html", {})

@require_GET
def select_page(request):
    return render(request, "select-page.html", {})

pageSize = 4
@require_GET
def post_page(request, pageNumber = 1, category = 'all', sortBy = 'newest'):
    allPost = Post.objects.all()
    paginator = Paginator(allPost, pageSize)
    totalPage = paginator.num_pages
    minPage = max(pageNumber - 2, 1)
    maxPage = min(pageNumber + 2, totalPage)
    rangePage = range(minPage, maxPage+1)
    posts = paginator.get_page(pageNumber)
    return render(request, 'post-page.html', {
        "posts" : posts,
        "rangePage": rangePage,
        'currentPage': pageNumber
    })

@require_GET
def post_view_page(request, postId):
    post = Post.objects.get(id = postId)
    data = {
        "post" : post
    }
    return render(request, "post-view-page.html", data)
