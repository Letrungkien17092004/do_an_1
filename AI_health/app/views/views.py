from django.shortcuts import render
from django.views.decorators.http import require_GET
from ..models import Post

@require_GET
def index(request):
    return render(request, "home.html", {})

@require_GET
def chat_page(request):
    return render(request, "chat-page.html", {})

@require_GET
def select_page(request):
    return render(request, "select-page.html", {})

@require_GET
def post_page(request):
    return render(request, 'post-page.html', {})

@require_GET
def post_view_page(request):
    post = Post.objects.all()
    data = {}
    if len(post) > 0:
        post = post[0]
        data['post'] = post
    print(post)
    return render(request, "post-view-page.html", data)
