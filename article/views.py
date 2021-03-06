from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework import filters
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from article.models import Article, Category
from article.serializers import ArticleSerializer, CategorySerializer, ArticleResponseSerializer


@method_decorator(login_required(login_url='my_account_login'), name='dispatch')
class ArticleApiView(ListCreateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'author__username', 'category__name']

    def perform_create(self, serializer):
        return serializer.save(author=self.request.user)

    @swagger_auto_schema(responses={status.HTTP_200_OK: ArticleResponseSerializer()})
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    @swagger_auto_schema(responses={status.HTTP_200_OK: ArticleResponseSerializer()})
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


@method_decorator(login_required(login_url='my_account_login'), name='dispatch')
class SingleArticleApiView(RetrieveUpdateDestroyAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer


@method_decorator(login_required(login_url='my_account_login'), name='dispatch')
class CategoryApiView(ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description']


@method_decorator(login_required(login_url='my_account_login'), name='dispatch')
class SingleCategoryApiView(RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
