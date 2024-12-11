from django.shortcuts import render
from django.views.decorators.http import require_GET
from sqlService.helper import PostHelper, CategoriesHelper
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

pageSize = 3
@require_GET
def post_page(request, pageNumber = 1, category = 'all', sortBy = 'newest'):
    posts = PostHelper.getAll(pageNumber, category, sortBy)
    paginator = Paginator(posts, pageSize)
    totalPage = paginator.num_pages
    minPage = max(pageNumber - 2, 1)                                              
    maxPage = min(pageNumber + 2, totalPage)
    rangePage = range(minPage, maxPage+1)
    postInPage = paginator.get_page(pageNumber)
    categories = CategoriesHelper.getAll()
    
    return render(request, 'post-page.html', {
        "posts" : postInPage,
        "rangePage": rangePage,
        'currentPage': pageNumber,
        "categories": categories,
        "currentCategory": category,
        "currentSortBy": sortBy
    })

@require_GET
def post_view_page(request, postId):
    post = PostHelper.getById(postId)
    data = {
        "post" : post
    }
    return render(request, "post-view-page.html", data)
