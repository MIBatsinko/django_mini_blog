from django.urls import path, re_path, include
from . import views
from allauth.account import views as allauth_views

from .views import UserApiView, SingleUserApiView

urlpatterns = [
    path('', UserApiView.as_view(), name='view_users'),
    path('<int:pk>/', SingleUserApiView.as_view(), name='change_users'),
]
