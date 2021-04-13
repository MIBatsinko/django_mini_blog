from django.urls import path, re_path, include
from . import views

urlpatterns = [
    path('login/', views.user_login, name='account_login'),
    path('register/', views.register, name='account_signup'),
    path('logout/', views.LogoutView.as_view(), name='account_logout'),
    path('', views.dashboard, name='dashboard'),
]
