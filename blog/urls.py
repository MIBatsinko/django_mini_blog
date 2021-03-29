from django.urls import path

from . import views
from comment import views as comment_views

urlpatterns = [
    path('', views.BlogHomePage.home, name='blog_index'),
    path('add_post', views.create, name='blog_add'),
    path('<int:pk>', views.NewsDetailView.as_view(), name='blog_view'),
    path('<int:pk>/update', views.NewsUpdateView.as_view(), name='blog_edit'),
    path('<int:pk>/delete', views.NewsDeleteView.as_view(), name='blog_delete'),
    path("add-rating/", views.AddStarRating.as_view(), name='add_rating'),

    path('<slug:username>/profile/<int:user_id>/', views.profile, name='profile'),
    path('profile_settings/<int:pk>', views.profile_settings, name="profile_settings"),

    path('<slug:article>/comments', comment_views.CommentsDetailView.as_view(), name='comments_view'),
    path('comment/<int:pk>/edit', comment_views.CommentUpdateView.as_view(), name='comment_edit'),
    path('<int:pk>/comment/delete', comment_views.CommentDeleteView.as_view(), name='comment_delete'),
    path('<slug:article>/comment_add/<slug:author>/', comment_views.comment_add, name='comment_add'),
]
