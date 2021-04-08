from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.AdminHome.home, name='admin_index'),
    path('user_info/', views.AdminUserProfile.info, name='user_info'),
    path('articles/', include([
        path('', views.AdminArticles.show_all, name='articles'),
        path('add/', views.AdminArticles.add, name='article_add'),
        path('edit/<int:pk>/', views.AdminArticleUpdateView.as_view(), name='article_edit'),
        path('delete/<int:pk>/', views.AdminArticleDeleteView.as_view(), name='article_delete'),
    ])),

]
