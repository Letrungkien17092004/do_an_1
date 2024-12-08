from django.urls import path
from .views import index, chat_page, post_page, post_view_page, select_page

urlpatterns = [
    path("", index, name="index"),
    path("prediction/chat/", chat_page, name="chat_page"),
    path("prediction/select/", select_page, name="select_page"),
    path("post/page/<int:pageNumber>", post_page, name="post_page"),
    path("post/page/", post_page, name="post_page"),
    path("post/view/<int:postId>", post_view_page, name="post_view_page"),
]