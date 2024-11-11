from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_GET
from django.views.decorators.csrf import csrf_exempt
import json
from DiseaseSystem.diseasePredictSys import DiseasePredictSys, Translator

@require_GET
def home(request):
    return render(request, "home.html", {})

@require_GET
def chat_page(request):
    return render(request, "chat-page.html", {})

@require_GET
def select_page(request):
    return render(request, "select-page.html", {})

@require_POST
@csrf_exempt
def messageHandler(request):
    # body = json.loads(request.body)
    # message_vi = "tôi bị nổi mẩn da và ngứa da"
    res = {
        "message": "Hệ thống hiện đang bận vui lòng thử lại sau"
    }
    return JsonResponse(res)

@require_POST
@csrf_exempt
def selectHandler(request):
    body = json.loads(request.body)
    print(body)
    res = {
        "message": "api select đã nhận và phản hồi lại thôn báo này"
    }
    return JsonResponse(res)