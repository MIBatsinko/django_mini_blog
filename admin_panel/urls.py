from django.urls import path

from . import views

urlpatterns = [
    path('', views.AdminHome.home, name='admin_index'),
    path('user_info/', views.User.info, name='user_info')
]
