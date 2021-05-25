from django.urls import path

import blog.views as views
from users.views import RatingUserPageView, UserProfilePageView, UserProfileUpdateView

urlpatterns = [
    path('', views.HomePage.home, name='index'),
    # path('blog/', views.ArticlesView.as_view(), name='blog_index'),
    path('blog/', views.Blog.articles, name='blog_index'),

    path('add_post/', views.ArticleCreateView.as_view(), name='blog_add'),
    path('<int:pk>/', views.ArticleDetailView.as_view(), name='blog_view'),
    path('<int:pk>/update/', views.ArticleUpdateView.as_view(), name='blog_edit'),
    path('<int:pk>/delete/', views.ArticleDeleteView.as_view(), name='blog_delete'),
    path("add-rating/", views.AddStarRating.as_view(), name='add_rating'),

    path("card_edit/", views.CardEdit.post, name='card_edit'),
    path("change_card/", views.CardChange.post, name='change_card'),

    path("rating_user/", RatingUserPageView.as_view(), name='rating_user'),
    path('profile/', UserProfilePageView.as_view(), name='profile'),
    path('profile_settings/', UserProfileUpdateView.as_view(), name="profile_settings"),

]
