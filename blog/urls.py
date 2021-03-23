from django.urls import path

from . import views

urlpatterns = [
    path('', views.news_home, name='blog_index'),
    path('add_post', views.create, name='blog_add'),
    path('<int:pk>', views.NewsDetailView.as_view(), name='blog_view'),
    path('<int:pk>/update', views.NewsUpdateView.as_view(), name='blog_edit'),
    path('<int:pk>/delete', views.NewsDeleteView.as_view(), name='blog_delete'),
]
