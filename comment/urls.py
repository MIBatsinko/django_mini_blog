from django.urls import path

from comment.views import SingleCommentApiView, CommentApiView
import comment.views as views


urlpatterns = [
    path('<int:pk>/edit/', views.CommentEdit.post, name='comment_edit'),
    path('<int:pk>/delete/', views.CommentDeleteView.as_view(), name='comment_delete'),
    path('<int:article_id>/comment_add/', views.CommentCreateView.as_view(), name='comment_add'),
    path('', CommentApiView.as_view(), name='view_comments'),
    path('<int:pk>/', SingleCommentApiView.as_view(), name='change_comments'),
]
