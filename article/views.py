# from django_filters import rest_framework as filters
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions, status
from rest_framework import filters
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from django.db import models

from .models import Article, Category
from .serializers import ArticleSerializer, CategorySerializer#, ArticleResponseSerializer


class ArticleApiView(ListCreateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'author__username', 'category__name']

    def perform_create(self, serializer):
        return serializer.save(author=self.request.user)

    # @swagger_auto_schema(responses={status.HTTP_200_OK: ArticleResponseSerializer()})
    # def post(self, request, *args, **kwargs):
    #     return self.create(request, *args, **kwargs)
    #
    # @swagger_auto_schema(responses={status.HTTP_200_OK: ArticleResponseSerializer()})
    # def get(self, request, *args, **kwargs):
    #     return self.list(request, *args, **kwargs)


class SingleArticleApiView(RetrieveUpdateDestroyAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer


class CategoryApiView(ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description']


class SingleCategoryApiView(RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
