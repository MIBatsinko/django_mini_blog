from django.shortcuts import render, redirect
from article.models import Article, Author
from .forms import ArticlesForm
from django.views.generic import DetailView, UpdateView, DeleteView


def news_home(request):
    blog = Article.objects.all()

    num_authors = Author.objects.count()  # The 'all()' is implied by default.

    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    return render(request, 'blog/blog_index.html', {"blog": blog, 'num_visits': num_visits})


class NewsDetailView(DetailView):
    model = Article
    template_name = 'blog/blog_view.html'
    context_object_name = 'article'


class NewsUpdateView(UpdateView):
    model = Article
    template_name = 'blog/blog_add.html'

    form_class = ArticlesForm


class NewsDeleteView(DeleteView):
    model = Article
    success_url = '/blog/'
    template_name = 'blog/blog_delete.html'


def create(request):
    error = ''
    if request.method == "POST":
        form = ArticlesForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('blog_index')
        else:
            error = "Invalid form"

    form = ArticlesForm()

    data = {
        'form': form,
        'error': error,
    }
    return render(request, 'blog/blog_add.html', data)
