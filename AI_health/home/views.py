from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_GET
from django.views.decorators.csrf import csrf_exempt
import json
from DiseaseSystem.diseasePredictSys import DiseasePredictSys

diseasePredictSys = DiseasePredictSys()
diseasePredictSys.load()

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
    raw_inp = json.loads(request.body)
    result = diseasePredictSys.diseasePredict(raw_inp, predType="select")
    res = {
        "message": result
    }
    return JsonResponse(res)