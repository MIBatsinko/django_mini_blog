from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views.generic.base import View
from django.contrib.auth.models import User
from django.views.generic import DetailView, UpdateView, DeleteView, CreateView, ListView
from rest_framework import status



from rest_framework.generics import get_object_or_404
from rest_framework.reverse import reverse_lazy

from article.models import Article, Category
from comment.models import Comment
from payments.services.stripe_service import Stripe
from blog.forms import ArticlesForm, RatingForm
from blog.models import Rating


class HomePageView(View):
    def get(self, request):
        # table of premium articles
        max_premium_articles = 6
        articles_list = Article.objects.filter(author__memberaccount__account_type="Premium").order_by('-date')[:max_premium_articles]

        return render(request, 'blog/index.html', {'articles_list': articles_list})


# class ArticlesListView(View):
#     def get(self, request):
#         articles = Article.objects.order_by('-date')
#         categories = Category.objects.all()
#
#         return render(request, 'blog/blog-list.html', {"articles": articles, 'categories': categories})


class ArticlesListView(ListView):
    model = Article
    template_name = 'blog/blog-list.html'
    context_object_name = 'articles'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()

        articles = Article.objects.order_by('-date')
        paginator = Paginator(articles, self.paginate_by)
        page = self.request.GET.get('page')
        try:
            articles_list = paginator.page(page)
        except PageNotAnInteger:
            articles_list = paginator.page(1)
        except EmptyPage:
            articles_list = paginator.page(paginator.num_pages)

        context['articles'] = articles_list
        return context


class ArticleDetailView(DetailView):
    model = Article
    template_name = 'blog/blog-single.html'
    context_object_name = 'article'

    def get_context_data(self, **kwargs):
        context = super(ArticleDetailView, self).get_context_data(**kwargs)
        context['comments'] = Comment.objects.filter(article=kwargs.get('object'))
        context['articles'] = Article.objects.order_by("-date")
        try:
            context['mark'] = Rating.objects.get(user=self.request.user.id, article=kwargs.get('object'))
        except Exception as e:
            print(e)
            context['mark'] = 0
        return context


@method_decorator(login_required(login_url='my_account_login'), name='dispatch')
class ArticleUpdateView(UpdateView):
    model = Article
    template_name = 'blog/add-article.html'
    context_object_name = 'article'
    form_class = ArticlesForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


@method_decorator(login_required(login_url='my_account_login'), name='dispatch')
class ArticleDeleteView(DeleteView):
    model = Article
    success_url = '/blog/'
    template_name = 'blog/blog_delete.html'


@method_decorator(login_required(login_url='my_account_login'), name='dispatch')
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
    template_name = 'blog/add-article.html'
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


class CardChange(View):
    def post(self, request):
        try:
            token = Stripe.stripe_api().Token.retrieve(request.POST.get('stripeToken', None))
            stripe = Stripe(request.user)
            stripe.create_source(token)
        except Exception as e:
            print(e)
        #     TODO: return error

        return redirect(reverse_lazy('profile'))
