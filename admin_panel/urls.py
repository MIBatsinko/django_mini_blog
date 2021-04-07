from django.urls import path

from . import views

urlpatterns = [
    path('', views.BlogHomePage.home, name='blog_index'),
    path('user_info/', views.User.info, name='user_info')
]
