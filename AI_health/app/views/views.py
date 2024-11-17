from django.shortcuts import render
from django.views.decorators.http import require_GET


@require_GET
def index(request):
    return render(request, "home.html", {})

@require_GET
def chat_page(request):
    return render(request, "chat-page.html", {})

@require_GET
def select_page(request):
    return render(request, "select-page.html", {})

