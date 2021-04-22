# from django_filters import rest_framework as filters
from rest_framework import permissions
from rest_framework import filters
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from django.db import models

from .models import Article
from .serializers import ArticleSerializer


class ArticleApiView(ListCreateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'author__username', 'category__name']

    def perform_create(self, serializer):
        return serializer.save(author=self.request.user)


class SingleArticleApiView(RetrieveUpdateDestroyAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
