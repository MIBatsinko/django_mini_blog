from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from .models import Article
from .serializers import ArticleSerializer


class ArticleApiView(ListCreateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    def perform_create(self, serializer):
        return serializer.save(author=self.request.user)


class SingleArticleApiView(RetrieveUpdateDestroyAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    def filter_queryset(self, queryset):
        queryset = self.queryset.filter(author=self.request.user)
        return queryset
