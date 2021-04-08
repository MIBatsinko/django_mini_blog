from django.urls import path

from . import views

urlpatterns = [
    path('', views.AdminHome.home, name='admin_index'),
    path('user_info/', views.AdminUserProfile.info, name='user_info'),
    path('articles/', views.AdminArticles.show_all, name='articles'),

]
