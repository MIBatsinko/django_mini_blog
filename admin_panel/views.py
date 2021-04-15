from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import UpdateView, DeleteView, DetailView, TemplateView, CreateView
from django.db import models
from rest_framework.reverse import reverse_lazy
import sweetify

from article.forms import CategoriesForm
from article.models import Article, Category
from blog.forms import UserProfileForm, ArticlesForm, RatingForm, UserForm
from blog.models import UserProfile, Rating
from comment.forms import CommentsForm
from comment.models import Comment
from sendemail.views import SendingEmail


class AdminHome(TemplateView):
    template_name = 'admin_panel/dashboard.html'


class AdminUsersView(TemplateView):
    template_name = 'admin_panel/users/users.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users'] = UserProfile.objects.all()
        return context


class AdminUserProfileView(TemplateView):
    template_name = 'admin_panel/users/user_info.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['select_user'] = User.objects.get(id=kwargs.get('pk'))
        return context


class AdminUserProfileUpdateView(UpdateView):
    model = UserProfile
    template_name = 'admin_panel/users/user_edit.html'
    success_url = '/admin_panel/users/'

    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        user = User.objects.get(id=pk)
        user_profile_form = UserProfileForm(initial={
                'avatar': user.userprofile.avatar,
            })
        user_form = UserForm(initial={
                'first_name': user.first_name,
                'email': user.email
            })
        context = {
            'user_profile_form': user_profile_form,
            'user_form': user_form,
            'user_profile': user.userprofile
        }
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        user = User.objects.get(id=pk)
        user_profile_form = UserProfileForm(self.request.POST, self.request.FILES, instance=user.userprofile)
        user_form = UserForm(self.request.POST, instance=user)
        if user_profile_form.is_valid() and user_form.is_valid():
            user_instance = user_form.save(commit=False)
            user_instance.first_name = user_form.cleaned_data.get('first_name')
            user_instance.email = user_form.cleaned_data.get('email')
            user_instance.is_staff = self.request.POST.get('is_staff', False)
            user_instance.is_active = self.request.POST.get('is_active', False)
            user_instance.is_superuser = self.request.POST.get('is_superuser', False)
            user_instance.save()

            userprofile_instance = user_profile_form.save(commit=False)
            userprofile_instance.avatar = user_profile_form.cleaned_data.get('avatar')
            userprofile_instance.save()
            return redirect('users')


class AdminUsersDeleteView(DeleteView):
    model = User
    success_url = '/admin_panel/users/'
    template_name = 'admin_panel/users/user_delete.html'

    def get_context_data(self, **kwargs):
        context = super(AdminUsersDeleteView, self).get_context_data(**kwargs)
        context['user_profile'] = UserProfile.objects.all()
        return context


class AdminArticlesView(TemplateView):
    template_name = 'admin_panel/articles/articles.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['articles'] = Article.objects.order_by('-date')
        return context


class AdminArticleCreateView(CreateView):
    model = Article
    template_name = 'admin_panel/articles/article_add.html'
    form_class = ArticlesForm

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.author = self.request.user
        instance.save()
        return redirect(reverse_lazy('articles'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class AdminArticleDetailView(DetailView):
    model = Article
    template_name = 'admin_panel/articles/article_details.html'
    context_object_name = 'article'

    def get_queryset(self):
        articles = Article.objects.filter().annotate(
            rating_user=models.Count("ratings",
                                     filter=models.Q(ratings__user=self.request.user.id))
        ).annotate(
            middle_star=(models.Avg("ratings__star"))
        )
        return articles

    def get_context_data(self, **kwargs):
        context = super(AdminArticleDetailView, self).get_context_data(**kwargs)
        article = kwargs.get('object', None)
        if article:
            context['comments'] = Comment.objects.filter(article=article)
        return context


class AdminArticleUpdateView(UpdateView):
    model = Article
    template_name = 'admin_panel/articles/article_edit.html'
    form_class = ArticlesForm
    success_url = '/admin_panel/articles/'


class AdminArticleDeleteView(DeleteView):
    model = Article
    success_url = '/admin_panel/articles/'
    template_name = 'admin_panel/articles/article_delete.html'


class AdminCategoriesView(TemplateView):
    template_name = 'admin_panel/categories/categories.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class AdminCategoryCreateView(CreateView):
    model = Category
    template_name = 'admin_panel/categories/category_add.html'
    form_class = CategoriesForm
    success_url = '/admin_panel/categories/'


class AdminCategoryUpdateView(UpdateView):
    model = Category
    template_name = 'admin_panel/categories/category_edit.html'
    form_class = CategoriesForm
    success_url = '/admin_panel/categories/'


class AdminCategoryDeleteView(DeleteView):
    model = Category
    success_url = '/admin_panel/categories/'
    template_name = 'admin_panel/categories/category_delete.html'


class AdminCommentUpdateView(UpdateView):
    model = Comment
    template_name = 'admin_panel/comments/comment_add.html'
    form_class = CommentsForm
    success_url = '/admin_panel/articles/'


class AdminCommentDeleteView(DeleteView):
    model = Comment
    success_url = '/admin_panel/articles/'
    template_name = 'admin_panel/comments/comment_delete.html'


class AdminCommentCreateView(CreateView):
    model = Comment
    template_name = 'admin_panel/comments/comment_add.html'
    form_class = CommentsForm
    success_url = '/admin_panel/comments/'

    def form_valid(self, form):
        author = User.objects.get(id=self.request.user.id)
        article_id = self.kwargs.get('article_id')
        article = Article.objects.get(id=article_id)
        instance = form.save(commit=False)
        instance.article = article
        instance.author = author
        instance.save()

        email = SendingEmail()
        email.new_comment(article, author, instance.body)

        return redirect(reverse_lazy('article_details', (article_id, )))
        # return redirect('/admin_panel/articles/details/{}/'.format(article.id))
