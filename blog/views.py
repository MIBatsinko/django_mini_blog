from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views.generic.base import View
from django.contrib.auth.models import User
from django.views.generic import DetailView, UpdateView, DeleteView, CreateView
from rest_framework import status

from rest_framework.generics import get_object_or_404
from rest_framework.reverse import reverse_lazy

from article.models import Article, Category
from comment.models import Comment
from .forms import ArticlesForm, RatingForm
from .models import Rating


class BlogHomePage:
    def home(self):
        blog = Article.objects.order_by('-date')
        categories = Category.objects.all()

        # num_authors = Author.objects.count()  # The 'all()' is implied by default.
        # Number of visits to this view, as counted in the session variable.
        num_visits = self.session.get('num_visits', 0)
        self.session['num_visits'] = num_visits + 1

        return render(self, 'blog/blog_index.html', {"blog": blog, 'categories': categories, 'num_visits': num_visits})


class ArticleDetailView(DetailView):
    model = Article
    template_name = 'blog/blog_view.html'
    context_object_name = 'article'

    def get_context_data(self, **kwargs):
        context = super(ArticleDetailView, self).get_context_data(**kwargs)
        context['comments'] = Comment.objects.all()
        context['star_form'] = RatingForm()
        try:
            context['mark'] = Rating.objects.get(user=self.request.user.id, article=kwargs['object'].id)
        except Rating.DoesNotExist:
            context['mark'] = 0
        except AttributeError:
            context['mark'] = 0
        return context


@method_decorator(login_required(login_url='my_account_login'), name='dispatch')
class ArticleUpdateView(UpdateView):
    model = Article
    template_name = 'blog/blog_add.html'
    context_object_name = 'article'
    form_class = ArticlesForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


@method_decorator(login_required(login_url='my_account_login'), name='dispatch')
class ArticleDeleteView(DeleteView):
    model = Article
    success_url = '/'
    template_name = 'blog/blog_delete.html'


# @method_decorator(login_required(login_url='my_account_login'), name='dispatch')
class AddStarRating(View):
    def post(self, request):
        form = RatingForm(request.POST)
        if form.is_valid():
            Rating.objects.update_or_create(
                article_id=int(request.POST.get("article")),
                user=get_object_or_404(User, id=request.user.id),
                defaults={'star_id': int(request.POST.get("star"))}
            )
            return HttpResponse(status=status.HTTP_201_CREATED)
        else:
            return HttpResponse(status=status.HTTP_400_BAD_REQUEST)


@method_decorator(login_required(login_url='my_account_login'), name='dispatch')
class ArticleCreateView(CreateView):
    model = Article
    template_name = 'blog/blog_add.html'
    form_class = ArticlesForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

    def form_valid(self, form):
        category = get_object_or_404(Category, name=get_object_or_404(self.request.POST, 'category'))
        instance = form.save(commit=False)
        instance.author = self.request.user
        instance.category = category
        instance.save()
        return redirect(reverse_lazy('blog_index'))
