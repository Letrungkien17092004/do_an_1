from django.urls import path
from .views import views
from .apis import predictAPI
from django.conf.urls.static import static

viewsURL = [
    path("", views.index, name="index"),
    path("prediction/chat/", views.chat_page, name="chat_page"),
    path("prediction/select/", views.select_page, name="select_page"),
]

apisURL = [
    path("api/predict/message", predictAPI.predictMassage, name="predictMassage"),
    path("api/predict/select", predictAPI.predictSelect, name="predictSelect"),
]
urlpatterns = viewsURL + apisURL