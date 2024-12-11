from django.urls import path
from .views import GetDiseaseInfo

urlpatterns = [
    path("disease/info/<str:diseaseName>", GetDiseaseInfo, name="getDiseaseInfo")
]