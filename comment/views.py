from django.shortcuts import render, redirect
from django.views.generic import DetailView, UpdateView, DeleteView, CreateView
from rest_framework import viewsets, filters
from rest_framework.generics import get_object_or_404, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.reverse import reverse_lazy

from article.models import Article
from django.contrib.auth.models import User

from .models import Comment
from .serializers import CommentSerializer
from .forms import CommentsForm


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()

    def filter_queryset(self, queryset):
        if self.request.method in ['PATCH', 'PUT', 'DELETE']:
            queryset = queryset.filter(author=self.request.user)
        return queryset


class CommentsDetailView(DetailView):
    model = Comment
    template_name = 'blog/blog_view.html'
    context_object_name = 'comment'
    slug_field = 'article'
    slug_url_kwarg = 'article'

    def get_context_data(self, **kwargs):
        context = super(CommentsDetailView, self).get_context_data(**kwargs)
        context['article'] = Article.objects.all()
        return context


class CommentUpdateView(UpdateView):
    model = Comment
    template_name = 'comment/comment_add.html'
    form_class = CommentsForm
    success_url = '/'


class CommentDeleteView(DeleteView):
    model = Comment
    success_url = '/'
    template_name = 'comment/comment_delete.html'


class CommentCreateView(CreateView):
    model = Comment
    template_name = 'comment/comment_add.html'
    form_class = CommentsForm
    success_url = '/blog/comments/'

    def form_valid(self, form):
        author = get_object_or_404(User, id=self.request.user.id)
        article_id = get_object_or_404(self.kwargs, 'article_id')
        article = get_object_or_404(Article, id=article_id)
        instance = form.save(commit=False)
        instance.article = article
        instance.author = author
        instance.save()

        return redirect(reverse_lazy('blog_view', (article_id, )))


class CommentApiView(ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description']


class SingleCommentApiView(RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

