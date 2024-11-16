from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("prediction/chat/", views.chat_page, name="chat-page"),
    path("prediction/select/", views.select_page, name="select-page"),
    path("api/message", views.messageHandler, name="messageHandler"),
    path("api/select", views.selectHandler, name="selectHandler"),
]