from django.urls import path

from .views import ArticleView, ArticleViewEdit

app_name = "articles"

urlpatterns = [
    path('articles/', ArticleView.as_view()),
    path('articles/<int:pk>/', ArticleViewEdit.as_view()),
]
