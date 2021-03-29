from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import CommentViewSet
from . import views


router = DefaultRouter()
router.register(r'comments', CommentViewSet, basename='user')

urlpatterns = router.urls

urlpatterns += [
    path('<slug:article>/comments', views.CommentsDetailView.as_view(), name='comments_view'),
    path('comment/<int:pk>/edit', views.CommentUpdateView.as_view(), name='comment_edit'),
    path('<int:pk>/comment/delete', views.CommentDeleteView.as_view(), name='comment_delete'),
    path('<slug:article>/comment_add/<slug:author>/', views.comment_add, name='comment_add'),
]
