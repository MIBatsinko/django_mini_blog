from django.urls import path

from .views import ArticleApiView, SingleArticleApiView


app_name = "articles"

urlpatterns = [
    path('', ArticleApiView.as_view()),
    path('<int:pk>/', SingleArticleApiView.as_view()),
]
