from django.shortcuts import render, redirect
from django.views.generic import DetailView, UpdateView, DeleteView
from rest_framework import viewsets

from .models import Comment
from .serializers import CommentSerializer
from .forms import CommentsForm


class CommentViewSet(viewsets.ModelViewSet):

    serializer_class = CommentSerializer
    queryset = Comment.objects.all()


def comment_add(request):
    error = ''
    if request.method == "POST":
        form = CommentsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('blog_view')
        else:
            error = "Invalid form"

    form = CommentsForm()

    data = {
        'form': form,
        'error': error,
    }
    return render(request, 'blog/blog_add.html', data)
