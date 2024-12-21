from django.urls import path
from .views import MedicineRecogniteView, TestA

urlpatterns = [
    path("v1/search-medicine", MedicineRecogniteView.as_view(), name ="medicine_search"),
]