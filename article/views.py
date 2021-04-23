# from django_filters import rest_framework as filters
from rest_framework import permissions
from rest_framework import filters
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from django.db import models

from .models import Article, Category
from .serializers import ArticleSerializer, CategorySerializer


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


class CategoryApiView(ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def perform_create(self, serializer):
        return serializer.save(author=self.request.user)


class SingleCategoryApiView(RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
