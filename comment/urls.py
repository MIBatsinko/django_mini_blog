from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import CommentViewSet
from . import views


router = DefaultRouter()
router.register('', CommentViewSet, basename='user')

urlpatterns = router.urls

urlpatterns += [
    path('<int:article>/', views.CommentsDetailView.as_view(), name='comments_view'),
    path('<int:pk>/edit', views.CommentUpdateView.as_view(), name='comment_edit'),
    path('<int:pk>/delete', views.CommentDeleteView.as_view(), name='comment_delete'),
    path('<int:article_id>/comment_add/', views.CommentCreateView.as_view(), name='comment_add'),
]
