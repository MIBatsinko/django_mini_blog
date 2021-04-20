from django_filters import rest_framework as filters
from rest_framework import permissions
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from django.db import models

from .models import Article
from .serializers import ArticleSerializer


# def get_queryset(self):
#     queryset = Article.objects.all()
#     title = self.request.query_params.get('title')
#     author = self.request.query_params.get('author')
#     category = self.request.query_params.get('category')
#
#     if title:
#         queryset = queryset.filter(title=title)
#     elif author:
#         queryset = queryset.filter(author__username=author)
#     elif category:
#         queryset = queryset.filter(category__name=category)
#
#     return queryset


# class ArticleFilter(filters.FilterSet):
#     class Meta:
#         model = Article
#         fields = ['title', 'author', 'category']


class ArticleApiView(ListCreateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    # filter_backends = (django_filters.rest_framework.DjangoFilterBackend, )
    filterset_fields = ['title', 'author__username', 'category__name']  # ?author__username=admin

    def perform_create(self, serializer):
        return serializer.save(author=self.request.user)


class SingleArticleApiView(RetrieveUpdateDestroyAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
