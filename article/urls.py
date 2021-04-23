from django.urls import path

from .views import ArticleApiView, SingleArticleApiView, CategoryApiView, SingleCategoryApiView


urlpatterns = [
    path('', ArticleApiView.as_view(), name='view_articles'),
    path('<int:pk>/', SingleArticleApiView.as_view(), name='change_articles'),
    path('categories/', CategoryApiView.as_view(), name='view_categories'),
    path('categories/<int:pk>/', SingleCategoryApiView.as_view(), name='change_categories'),
]
