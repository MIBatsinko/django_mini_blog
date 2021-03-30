from rest_framework import permissions
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from django.db import models

from .models import Article
from .serializers import ArticleSerializer


class ArticleApiView(ListCreateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    def get_queryset(self):
        articles = Article.objects.filter().annotate(
            rating_user=models.Count("ratings",
                                     filter=models.Q(ratings__ip=self.get_client_ip(self.request)))
        ).annotate(
            middle_star=(models.Avg("ratings__star"))
        )
        print(articles)
        return articles




    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    #
    # permission_classes = [permissions.IsAuthenticated]
    #
    # def get_queryset(self):
    #     movies = Article.objects.filter().annotate(
    #         rating_user=models.Count("ratings",
    #                                  filter=models.Q(ratings__ip=self.get_client_ip(self.request)))
    #     ).annotate(
    #         middle_star=models.Sum(models.F('ratings__star')) / models.Count(models.F('ratings'))
    #     )
    #     return movies

    def perform_create(self, serializer):
        return serializer.save(author=self.request.user)


class SingleArticleApiView(RetrieveUpdateDestroyAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    def filter_queryset(self, queryset):
        queryset = self.queryset.filter(author=self.request.user)
        return queryset
