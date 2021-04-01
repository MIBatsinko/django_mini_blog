from django.urls import path

from . import views
from comment import views as comment_views

urlpatterns = [
    path('', views.BlogHomePage.home, name='blog_index'),
    path('add_post', views.ArticleAdd.create, name='blog_add'),
    path('<int:pk>', views.ArticleDetailView.as_view(), name='blog_view'),
    path('<int:pk>/update', views.ArticleUpdateView.as_view(), name='blog_edit'),
    path('<int:pk>/delete', views.ArticleDeleteView.as_view(), name='blog_delete'),
    path("add-rating/", views.AddStarRating.as_view(), name='add_rating'),

    path("rating_user/", views.RatingUserPage.show_rating, name='rating_user'),
    path('profile/', views.UserProfilePage.profile, name='profile'),
    path('profile_settings/', views.UserProfileSettings.profile_settings, name="profile_settings"),
]
