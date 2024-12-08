from django.urls import path
from predictService.views import predictSelect, predictMassage

urlpatterns = [
    path("message", predictMassage, name="predictMassage"),
    path("select", predictSelect, name="predictSelect"),
]