from rest_framework.generics import get_object_or_404, ListCreateAPIView, RetrieveUpdateDestroyAPIView

from .models import Article
from django.contrib.auth.models import User
from .serializers import ArticleSerializer


class ArticleApiView(ListCreateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    def perform_create(self, serializer):
        # author = get_object_or_404(User, id=self.request.data.get('user_id'))
        return serializer.save(author=self.request.user)


class SingleArticleApiView(RetrieveUpdateDestroyAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    def filter_queryset(self, queryset):
        queryset = self.queryset.filter(author=self.request.user)
        return queryset
