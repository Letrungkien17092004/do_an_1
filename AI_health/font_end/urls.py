from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"), # Home

    path("prediction/chat/", views.chat_page, name="chat_page"), # Prediction chat
    path("prediction/select/", views.select_page, name="select_page"), # Prediction select

    path("post/page/<int:pageNumber>/<str:category>/<str:sortBy>", views.post_page, name="post_page"), # Post
    path("post/page/", views.post_page, name="post_page"),
    path("post/view/<int:postId>", views.post_view_page, name="post_view_page"),

    path("tra-cuu-thuoc", views.medicine_search, name="medicine_search")

]