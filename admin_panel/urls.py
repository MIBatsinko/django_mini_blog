from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.AdminHome.home, name='admin_index'),
    path('user_info/', views.AdminUserProfile.info, name='user_info'),
    path('articles/', include([
        path('', views.AdminArticles.show_all, name='articles'),
        path('add/', views.AdminArticles.add, name='article_add'),
        path('edit/', views.AdminArticles.edit, name='article_edit'),
        path('delete/', views.AdminArticles.delete, name='article_delete'),
    ])),

]
