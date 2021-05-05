from django.urls import path

import blog.views as views


urlpatterns = [
    path('', views.BlogHomePage.home, name='blog_index'),
    path('add_post/', views.ArticleCreateView.as_view(), name='blog_add'),
    path('<int:pk>/', views.ArticleDetailView.as_view(), name='blog_view'),
    path('<int:pk>/update/', views.ArticleUpdateView.as_view(), name='blog_edit'),
    path('<int:pk>/delete/', views.ArticleDeleteView.as_view(), name='blog_delete'),
    path("add-rating/", views.AddStarRating.as_view(), name='add_rating'),

    path("rating_user/", views.RatingUserPageView.as_view(), name='rating_user'),
    path('profile/', views.UserProfilePageView.as_view(), name='profile'),
    path('profile_settings/', views.UserProfileUpdateView.as_view(), name="profile_settings"),

]
