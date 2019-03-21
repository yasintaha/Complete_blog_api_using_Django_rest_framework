from django.urls import path
from api.views import (PostView,
                        PostListView,
                        PostUpdateView,
                        PostDeleteView,
                        PostDetailView,
                        PostPublish,
                        add_comment_to_post,
                        comment_approve,
                        comment_remove,
                        commentList,
                        SignupView,
                        LoginView)

urlpatterns = [
    path('Register/',SignupView.as_view()),
    path('Login/',LoginView.as_view()),
    path('newpost/',PostView.as_view()),
    path('Listpost/',PostListView.as_view()),
    path('post_update/<int:pk>/',PostUpdateView.as_view()),
    path('post_delete/<int:pk>/',PostDeleteView.as_view()),
    path('post_detail/<int:pk>/',PostDetailView.as_view()),
    path('post_publish/<int:pk>/',PostPublish.as_view()),
    path('add_comment/',add_comment_to_post.as_view()),
    path('comment_list/',commentList.as_view()),
    path('comment_approve/<int:pk>/',comment_approve.as_view()),
    path('comment_remove/<int:pk>/',comment_remove.as_view()),
]