from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

@require_POST
@csrf_exempt
def search(request):
    return JsonResponse({
        "message:" "OK",
        "medicineInfo:" "INFO"
    })