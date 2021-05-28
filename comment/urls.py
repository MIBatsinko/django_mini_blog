from django.urls import path

from comment.views import SingleCommentApiView, CommentApiView, CommentCreateView, CommentDeleteView, CommentEdit

urlpatterns = [
    path('<int:pk>/edit/', CommentEdit.post, name='comment_edit'),
    path('<int:pk>/delete/', CommentDeleteView.as_view(), name='comment_delete'),
    path('<int:article_id>/comment_add/', CommentCreateView.as_view(), name='comment_add'),
    path('', CommentApiView.as_view(), name='view_comments'),
    path('<int:pk>/', SingleCommentApiView.as_view(), name='change_comments'),
]
