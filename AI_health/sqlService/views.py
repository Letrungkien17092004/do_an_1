from django.shortcuts import render
from django.http import JsonResponse
from .helper import DiseaseHelper
# Create your views here.

def GetDiseaseInfo(request, diseaseName):
    result = DiseaseHelper.getDiseaseInfo(diseaseName)
    return JsonResponse({
        "result" : result,
        "status": "OK"
    })

