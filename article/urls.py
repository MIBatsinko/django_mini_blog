from django.urls import path

from .views import ArticleApiView, SingleArticleApiView


urlpatterns = [
    path('', ArticleApiView.as_view(), name='view_articles'),
    path('<int:pk>/', SingleArticleApiView.as_view(), name='change_articles'),
]
