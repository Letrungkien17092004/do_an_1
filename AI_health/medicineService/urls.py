from django.urls import path
# from .views import MedicineRecogniteView
from .views import medicineSearch

urlpatterns = [
    # path("v1/search-medicine", MedicineRecogniteView.as_view(), name ="medicine_search"),
    path("v1/search-medicine", medicineSearch, name ="medicine_search"),
]