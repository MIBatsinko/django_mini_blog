from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import CommentViewSet
from . import views


router = DefaultRouter()
router.register(r'comments', CommentViewSet, basename='user')

urlpatterns = router.urls
