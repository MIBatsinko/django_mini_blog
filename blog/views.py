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
from miniblog.settings import CONSTANCE_CONFIG
from payments.models import MemberAccount
from payments.services.stripe_service import Stripe
from .forms import ArticlesForm, RatingForm
from .models import Rating


class HomePage:
    def home(self):
        # table of premium articles
        blog = Article.objects.filter(author__memberaccount__account_type="Premium").order_by('-date')
        left, right = [], []
        count = 0
        for article in blog:
            count += 1
            left.append(article) if count % 2 != 0 else right.append(article)
        if len(left) > len(right):
            right.append("")
        articles = zip(left, right)

        num_visits = self.session.get('num_visits', 0)
        self.session['num_visits'] = num_visits + 1

        return render(self, 'blog/index.html', {'num_visits': num_visits, 'articles': articles})


class Blog:
    def articles(self):
        blog = Article.objects.order_by('-date')
        categories = Category.objects.all()

        return render(self, 'blog/blog-list.html', {"article": blog, 'categories': categories})


# class ArticlesView(ListView):
#     model = Article
#     template_name = 'blog/blog-list.html'
#     context_object_name = 'article'
#
#     def get_context_data(self, **kwargs):
#         context = super(ArticlesView, self).get_context_data(**kwargs)
#         context['categories'] = Category.objects.all()
#         return context


class ArticleDetailView(DetailView):
    model = Article
    template_name = 'blog/blog-single.html'
    context_object_name = 'article'

    def get_context_data(self, **kwargs):
        context = super(ArticleDetailView, self).get_context_data(**kwargs)
        context['comments'] = Comment.objects.filter(article=kwargs.get('object').id)
        context['star_form'] = RatingForm()
        context['categories'] = Category.objects.all()
        context['articles'] = Article.objects.order_by("-date")
        context['rating_stars'] = [i for i in range(CONSTANCE_CONFIG.get('RATING')[0], 0, -1)]
        try:
            context['mark'] = Rating.objects.get(user=self.request.user.id, article=kwargs.get('object').id)
        except Rating.DoesNotExist:
            context['mark'] = 0
        except AttributeError:
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


class CardEdit:
    def post(self):
        memberaccount = MemberAccount.objects.filter(user_id=self.user.id)
        memberaccount.update(card_id=self.POST.get('card_value'))
        return redirect(reverse_lazy('profile'))


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
