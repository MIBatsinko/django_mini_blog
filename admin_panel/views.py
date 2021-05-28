from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.generic import UpdateView, DeleteView, DetailView, TemplateView, CreateView
from rest_framework.generics import get_object_or_404
from rest_framework.reverse import reverse_lazy
from django.conf import settings

from article.forms import CategoriesForm
from article.models import Article, Category
from blog.forms import ArticlesForm
from users.forms import UserProfileForm, UserForm
from comment.forms import CommentsForm
from comment.models import Comment
from users.models import UserProfile


@method_decorator(settings.DECORATORS, name='dispatch')
class AdminHome(TemplateView):
    template_name = 'admin_panel/dashboard.html'


@method_decorator(settings.DECORATORS, name='dispatch')
class AdminUsersView(TemplateView):
    template_name = 'admin_panel/users/users.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users'] = UserProfile.objects.all()
        return context


@method_decorator(settings.DECORATORS, name='dispatch')
class AdminUserProfileView(TemplateView):
    template_name = 'admin_panel/users/user_info.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['select_user'] = get_object_or_404(User, id=kwargs.get('pk'))
        return context


@method_decorator(settings.DECORATORS, name='dispatch')
class AdminUserProfileUpdateView(UpdateView):
    model = UserProfile
    template_name = 'admin_panel/users/user_edit.html'
    success_url = '/admin_panel/users/'

    def get(self, request, *args, **kwargs):
        pk = get_object_or_404(kwargs, 'pk')
        user = get_object_or_404(User, id=pk)
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
        pk = get_object_or_404(kwargs, 'pk')
        user = get_object_or_404(User, id=pk)
        user_profile_form = UserProfileForm(self.request.POST, self.request.FILES, instance=user.userprofile)
        user_form = UserForm(self.request.POST, instance=user)
        if user_profile_form.is_valid() and user_form.is_valid():
            user_instance = user_form.save(commit=False)
            user_instance.first_name = get_object_or_404(user_form.cleaned_data, 'first_name')
            user_instance.email = get_object_or_404(user_form.cleaned_data, 'email')
            user_instance.is_staff = get_object_or_404(self.request.POST, 'is_staff', False)
            user_instance.is_active = get_object_or_404(self.request.POST, 'is_active', False)
            user_instance.is_superuser = get_object_or_404(self.request.POST, 'is_superuser', False)
            user_instance.save()

            userprofile_instance = user_profile_form.save(commit=False)
            userprofile_instance.avatar = get_object_or_404(user_profile_form.cleaned_data, 'avatar')
            userprofile_instance.save()
            return redirect('users')


@method_decorator(settings.DECORATORS, name='dispatch')
class AdminArticlesView(TemplateView):
    template_name = 'admin_panel/articles/articles.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['articles'] = Article.objects.order_by('-date')
        return context


@method_decorator(settings.DECORATORS, name='dispatch')
class AdminArticleCreateView(CreateView):
    model = Article
    template_name = 'admin_panel/articles/article_add.html'
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
        return redirect(reverse_lazy('articles'))

    def form_invalid(self, form):
        response = super().form_invalid(form)
        if self.request.accepts('text/html'):
            return response


@method_decorator(settings.DECORATORS, name='dispatch')
class AdminArticleDetailView(DetailView):
    model = Article
    template_name = 'admin_panel/articles/article_details.html'
    context_object_name = 'article'

    def get_context_data(self, **kwargs):
        context = super(AdminArticleDetailView, self).get_context_data(**kwargs)
        article = kwargs.get('object', None)
        if article:
            context['comments'] = Comment.objects.filter(article=article)
        return context


@method_decorator(settings.DECORATORS, name='dispatch')
class AdminArticleUpdateView(UpdateView):
    model = Article
    template_name = 'admin_panel/articles/article_edit.html'
    form_class = ArticlesForm
    success_url = '/admin_panel/articles/'


@method_decorator(settings.DECORATORS, name='dispatch')
class AdminArticleDeleteView(DeleteView):
    model = Article
    success_url = '/admin_panel/articles/'
    template_name = 'admin_panel/articles/article_delete.html'


@method_decorator(settings.DECORATORS, name='dispatch')
class AdminCategoriesView(TemplateView):
    template_name = 'admin_panel/categories/categories.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


@method_decorator(settings.DECORATORS, name='dispatch')
class AdminCategoryCreateView(CreateView):
    model = Category
    template_name = 'admin_panel/categories/category_add.html'
    form_class = CategoriesForm
    success_url = '/admin_panel/categories/'


@method_decorator(settings.DECORATORS, name='dispatch')
class AdminCategoryUpdateView(UpdateView):
    model = Category
    template_name = 'admin_panel/categories/category_edit.html'
    form_class = CategoriesForm
    success_url = '/admin_panel/categories/'


@method_decorator(settings.DECORATORS, name='dispatch')
class AdminCategoryDeleteView(DeleteView):
    model = Category
    success_url = '/admin_panel/categories/'
    template_name = 'admin_panel/categories/category_delete.html'


@method_decorator(settings.DECORATORS, name='dispatch')
class AdminCommentUpdateView(UpdateView):
    model = Comment
    template_name = 'admin_panel/comments/comment_add.html'
    form_class = CommentsForm

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.save()
        return redirect(reverse_lazy('article_details', (instance.article.id,)))

    def form_invalid(self, form):
        response = super().form_invalid(form)
        if self.request.accepts('text/html'):
            return response


@method_decorator(settings.DECORATORS, name='dispatch')
class AdminCommentDeleteView(DeleteView):
    model = Comment
    success_url = '/admin_panel/articles/'
    template_name = 'admin_panel/comments/comment_delete.html'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        article_id = self.object.article.id
        self.object.delete()
        return redirect(reverse_lazy('article_details', (article_id,)))


@method_decorator(settings.DECORATORS, name='dispatch')
class AdminCommentCreateView(CreateView):
    model = Comment
    template_name = 'admin_panel/comments/comment_add.html'
    form_class = CommentsForm
    success_url = '/admin_panel/comments/'

    def form_valid(self, form):
        author = self.request.user
        article_id = get_object_or_404(self.kwargs, 'article_id')
        article = get_object_or_404(Article, id=article_id)

        instance = form.save(commit=False)
        instance.article = article
        instance.author = author
        instance.save()

        return redirect(reverse_lazy('article_details', (article_id, )))

    def form_invalid(self, form):
        response = super().form_invalid(form)
        if self.request.accepts('text/html'):
            return response


class AdminUserIsActive:
    @staff_member_required
    def deactivate(self, pk):
        user_id = get_object_or_404(User, id=pk)
        user_id.is_active = False
        user_id.save()
        return redirect('users')

    @staff_member_required
    def activate(self, pk):
        user_id = get_object_or_404(User, id=pk)
        user_id.is_active = True
        user_id.save()
        return redirect('users')
