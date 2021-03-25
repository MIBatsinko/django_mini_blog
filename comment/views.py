from django.shortcuts import render, redirect
from django.views.generic import DetailView, UpdateView, DeleteView
from rest_framework import viewsets
from rest_framework.generics import get_object_or_404

from article.models import Article, Author
from .models import Comment
from .serializers import CommentSerializer
from .forms import CommentsForm


class CommentViewSet(viewsets.ModelViewSet):

    serializer_class = CommentSerializer
    queryset = Comment.objects.all()


class CommentsDetailView(DetailView):
    model = Comment
    template_name = 'blog/blog_view.html'
    context_object_name = 'comment'
    slug_field = 'article'
    slug_url_kwarg = 'article'

    def get_context_data(self, **kwargs):
        ctx = super(CommentsDetailView, self).get_context_data(**kwargs)
        ctx['article'] = Article.objects.all()
        return ctx


class CommentUpdateView(UpdateView):
    model = Comment
    template_name = 'comment/comment_add.html'

    form_class = CommentsForm

    success_url = '/blog/'


class CommentDeleteView(DeleteView):
    model = Comment
    success_url = '/blog/'
    template_name = 'comment/comment_delete.html'


def comments_list(request):
    comment = Comment.objects.all()

    return render(request, 'comment/comment_view.html', {"comment": comment})


# class CommentUpdateView(UpdateView):
#     model = Comment
#     template_name = 'comment/comment_add.html'
#     slug_field = 'article'
#     #slug_url_kwarg = 'article'
#     form_class = CommentsForm


def comment_add(request, article):
    error = ''
    if request.method == "POST":
        form = CommentsForm(request.POST)
        print(form, form.is_valid())
        if form.is_valid():
            article_id = Article.objects.get(id=article)
            author_id = Author.objects.get(id=1)

            instance = form.save(commit=False)
            instance.article = article_id
            instance.author = author_id
            instance.save()
            return redirect('blog_index')
        else:
            error = "Invalid form"

    form = CommentsForm()

    data = {
        'form': form,
        'error': error,
    }
    return render(request, 'comment/comment_add.html', data)
