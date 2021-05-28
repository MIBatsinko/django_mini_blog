from django.urls import path

from blog.views import HomePageView, ArticlesListView, CardChange, AddStarRating, ArticleDeleteView, ArticleUpdateView, \
    ArticleDetailView, ArticleCreateView
from users.views import RatingUserPageView, UserProfilePageView, UserProfileUpdateView

urlpatterns = [
    path('', HomePageView.as_view(), name='index'),
    path('blog/', ArticlesListView.as_view(), name='blog_index'),

    path('add_post/', ArticleCreateView.as_view(), name='blog_add'),
    path('<int:pk>/', ArticleDetailView.as_view(), name='blog_view'),
    path('<int:pk>/update/', ArticleUpdateView.as_view(), name='blog_edit'),
    path('<int:pk>/delete/', ArticleDeleteView.as_view(), name='blog_delete'),
    path("add-rating/", AddStarRating.as_view(), name='add_rating'),

    path("change_card/", CardChange.as_view(), name='change_card'),

    path("rating_user/", RatingUserPageView.as_view(), name='rating_user'),
    path('profile/', UserProfilePageView.as_view(), name='profile'),
    path('profile_settings/', UserProfileUpdateView.as_view(), name="profile_settings"),

]
